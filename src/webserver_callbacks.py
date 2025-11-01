import urllib.parse

HTML_DAT = 'html_formatted'
RX_DAT   = '/project1/bird_board_micro/comms/web_rx'

def _update_rx(topic, value):
    """Update the RX table with received values"""
    rx = op(RX_DAT)
    if not rx:
        debug('RX table not found!')
        return

    found = False
    for r in range(rx.numRows):
        if rx[r, 0].val == topic:
            rx[r, 1] = value
            found = True
            break

    if not found:
        rx.appendRow([topic, value])

    debug(f"{topic} = {value}")

def _handle_command(topic, value):
    """Route commands to appropriate birdboard functions"""
    debug(f"Handling: {topic} = {value}")
    
    try:
        # Volume controls
        if topic in ('/vol_global', '/vol_birds', '/vol_ambi'):
            volume = float(value)
            row = topic.split('/')[-1]  # vol_global, vol_birds, vol_ambi
            op.birdboard_ctrl.op('volume')[row, 1] = volume
            debug(f'Set {row} = {volume:.2f}')
        
        # Playback controls
        elif topic == '/special':
            op.birdboard_comms.Special()
            
        elif topic == '/special_nature':
            op.birdboard_comms.SpecialNature()
            
        elif topic == '/normal':
            op.birdboard_comms.Normal()
            
        elif topic == '/stop':
            op.birdboard_comms.Stop()
            op.triggers.op('trigger_stop').par.triggerpulse.pulse()
        
        # Track selection
        elif topic == '/hotelcalifornia':
            op.birdboard_comms.HotelCalifornia()
            op.triggers.op('trigger_hotelcalifornia').par.triggerpulse.pulse()
            
        elif topic == '/likeavirgin':
            op.birdboard_comms.LikeAVirgin()
            op.triggers.op('trigger_likeavirgin').par.triggerpulse.pulse()
            
        elif topic == '/prettygirlrock':
            op.birdboard_comms.PrettyGirlRock()
            op.triggers.op('trigger_prettygirlrock').par.triggerpulse.pulse()
        
        # System controls
        elif topic == '/reboot':
            op.birdboard_comms.Reboot()
            op.triggers.op('trigger_reboot').par.triggerpulse.pulse()
            
        elif topic == '/shutdown':
            op.birdboard_comms.Shutdown()
            op.triggers.op('trigger_shutdown').par.triggerpulse.pulse()
        
        # Sync mode
        elif topic == '/sync':
            op('sync')[0,0] = 1
            debug('SYNC MODE enabled')
            
        elif topic == '/async':
            op('sync')[0,0] = 0
            debug('ASYNC MODE enabled')
            
        else:
            debug(f'Unknown command: {topic}')
    except Exception as e:
        debug(f'ERROR executing command: {e}')

def debug(msg):
    print('WEB | web_rx →', msg)

def onHTTPRequest(webServerDAT, request, response):
    # Use 'pars' instead of 'get' for query parameters in TouchDesigner
    path = request.get('uri', '/')  # 'uri' contains the full path
    method = request.get('method', 'GET')
    pars = request.get('pars', {})  # THIS IS THE KEY CHANGE
    
    # Parse path and query from URI if needed
    if '?' in path:
        path, query_string = path.split('?', 1)
        # Parse query string manually
        query_params = {}
        for param in query_string.split('&'):
            if '=' in param:
                key, val = param.split('=', 1)
                query_params[key] = [urllib.parse.unquote_plus(val)]
    else:
        query_params = pars
    
    # DETAILED DEBUGGING
    print('=' * 50)
    print(f'WEB | Method: {method}')
    print(f'WEB | Path: {path}')
    print(f'WEB | Pars: {pars}')
    print(f'WEB | Parsed query: {query_params}')
    print('=' * 50)

    # Serve the HTML page
    if path == '/' or path == '':
        html_op = op(HTML_DAT)
        if html_op is None:
            print(f'ERROR: Cannot find DAT named "{HTML_DAT}"')
            response['statusCode'] = 500
            response['data'] = b'HTML DAT not found'
            return response
            
        html = html_op.text.encode('utf-8')
        response['statusCode'] = 200
        response['headerDict'] = {'Content-Type': 'text/html; charset=utf-8'}
        response['data'] = html
        print(f'WEB | Served HTML ({len(html)} bytes)')
        return response

    # Handle control commands
    if path == '/set':
        print(f'WEB | /set endpoint hit!')
        print(f'WEB | Query params dict: {query_params}')
        
        topic = query_params.get('topic', [''])[0] if isinstance(query_params.get('topic', ['']), list) else query_params.get('topic', '')
        value = query_params.get('value', [''])[0] if isinstance(query_params.get('value', ['']), list) else query_params.get('value', '')
        
        topic = urllib.parse.unquote_plus(topic)
        value = urllib.parse.unquote_plus(value)
        
        print(f'WEB | Parsed topic: "{topic}"')
        print(f'WEB | Parsed value: "{value}"')
        
        if topic and value:
            _update_rx(topic, value)
            _handle_command(topic, value)
            response['statusCode'] = 200
            response['data'] = f'OK: {topic}={value}'.encode('utf-8')
        else:
            print('WEB | ERROR: Missing topic or value!')
            response['statusCode'] = 400
            response['data'] = b'Missing topic or value'
        
        return response

    # 404 for unknown paths
    print(f'WEB | 404 - Unknown path: {path}')
    response['statusCode'] = 404
    response['data'] = b'Not Found'
    return response

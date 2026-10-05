"""
============================================================
NOVA UI BRIDGE
============================================================

This bridge supports two situations:

1. Same-process communication
2. Separate Nova backend process

The PyQt UI receives events through a multiprocessing Queue.

Supported events:

- status
- network
- command
- response
- error
============================================================
"""

import threading


# ============================================================
# CALLBACKS
# ============================================================

_status_callback = None
_network_callback = None
_command_callback = None
_response_callback = None
_error_callback = None


# ============================================================
# EVENT QUEUE
# ============================================================

_event_queue = None


# ============================================================
# LOCK
# ============================================================

_bridge_lock = threading.RLock()


# ============================================================
# CONFIGURE EVENT QUEUE
# ============================================================

def set_event_queue(event_queue):

    global _event_queue

    with _bridge_lock:

        _event_queue = event_queue


# ============================================================
# CLEAR EVENT QUEUE
# ============================================================

def clear_event_queue():

    global _event_queue

    with _bridge_lock:

        _event_queue = None


# ============================================================
# REGISTER CALLBACKS
# ============================================================

def register_callbacks(
    status_callback=None,
    network_callback=None,
    command_callback=None,
    response_callback=None,
    error_callback=None
):

    global _status_callback
    global _network_callback
    global _command_callback
    global _response_callback
    global _error_callback


    with _bridge_lock:

        _status_callback = status_callback
        _network_callback = network_callback
        _command_callback = command_callback
        _response_callback = response_callback
        _error_callback = error_callback


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def register_ui(
    status_callback=None,
    command_callback=None,
    response_callback=None,
    error_callback=None
):

    register_callbacks(
        status_callback=status_callback,
        command_callback=command_callback,
        response_callback=response_callback,
        error_callback=error_callback
    )


# ============================================================
# CLEAR CALLBACKS
# ============================================================

def clear_callbacks():

    global _status_callback
    global _network_callback
    global _command_callback
    global _response_callback
    global _error_callback


    with _bridge_lock:

        _status_callback = None
        _network_callback = None
        _command_callback = None
        _response_callback = None
        _error_callback = None


# ============================================================
# INTERNAL EVENT SENDER
# ============================================================

def _send_event(event_type, value):

    global _event_queue


    # --------------------------------------------------------
    # Local callback
    # --------------------------------------------------------

    callback = None


    with _bridge_lock:

        if event_type == "status":

            callback = _status_callback


        elif event_type == "network":

            callback = _network_callback


        elif event_type == "command":

            callback = _command_callback


        elif event_type == "response":

            callback = _response_callback


        elif event_type == "error":

            callback = _error_callback


        queue = _event_queue


    # --------------------------------------------------------
    # Send to callback
    # --------------------------------------------------------

    if callback:

        try:

            callback(
                str(value)
            )

        except Exception as e:

            print(
                "[UI BRIDGE CALLBACK ERROR]",
                e
            )


    # --------------------------------------------------------
    # Send to PyQt process
    # --------------------------------------------------------

    if queue:

        try:

            queue.put(
                (
                    event_type,
                    str(value)
                ),
                block=False
            )

        except Exception as e:

            print(
                "[UI BRIDGE QUEUE ERROR]",
                e
            )


# ============================================================
# STATUS
# ============================================================

def emit_status(status):

    _send_event(
        "status",
        status
    )


# ============================================================
# NETWORK STATUS
# ============================================================

def emit_network_status(status):

    _send_event(
        "network",
        status
    )


# ============================================================
# USER COMMAND
# ============================================================

def emit_command(command):

    _send_event(
        "command",
        command
    )


# ============================================================
# NOVA RESPONSE
# ============================================================

def emit_response(response):

    _send_event(
        "response",
        response
    )


# ============================================================
# ERROR
# ============================================================

def emit_error(error):

    _send_event(
        "error",
        error
    )
#! /usr/bin/python3

def load_session():
    session = load_the_session_from_file()
    if not session:
        return None
    if session is expired:
        return None
    return session

def load_or_download_session():
    with lock:
        if session := load_session():
            return session
        session = get_session_with_auth()
        save_the_session(session)
        return session

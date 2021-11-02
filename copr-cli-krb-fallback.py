#! /bin/python

copr_instance = "fedora"
token = None

# python3-copr && copr-cli should use the same logic

if config_file:  # ~/.config/copr (or --config)
   # load instance (fedora/redhat/..), username, token, etc.
   ... = load_config_file()
     
if token is None:
    # How do we know the username for e.g. 'dnf build <projectname> local.src.rpm'?
    # Do we need it?
   
    # (temporarily?) notify that we use kerberos, can be opt-outed by config
    if not config.kerberos:
        log.info("Trying kerberos with %s", username)
        log.info("silence this by 'kerberos = True' in your config")
 
    # Go with kerberos log-in attempt because there's no token file.
else:
    # Go with token.  Token is preferred over kerberos, even if kerberos is
    # is available.

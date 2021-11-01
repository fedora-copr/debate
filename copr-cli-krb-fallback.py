#! /bin/python

copr_instance = "fedora"
token = None

if config_file:
   # load instance (fedora/redhat/..), username, token, etc.
   ... = load_config_file()
     
if token is None:
    # How do we know the username for e.g. 'dnf build <projectname> local.src.rpm'?
    # Do we need it?
   
    # (temporarily?) notify that we use kerberos, can be opt-outed by config
    if not config.kerberos:
        log.info("Trying kerberos with %s", username)
        log.info("silence this by 'kerberos = True' in your config")
 
    # Go with kerberos log-in attempt
else:
    # Go without kerberos here (old-code)

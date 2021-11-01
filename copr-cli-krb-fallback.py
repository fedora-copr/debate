#! /bin/python

copr_instance = "fedora"
if config_file:
   # load instance (fedora/redhat/..), username, token, etc.
   load_config_file()
  
if username is None:
   username = pwname()
   
if token is None:
    if not config.kerberos:
        log.info("trying kerberos with %s", username)
        log.info("silence this by kerberos = True in your config")
    # Go with kerberos log-in attempt
else:
    # Go without kerberos here (old-code)

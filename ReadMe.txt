
=============================================================
+Client_sms part
=============================================================

Files:

setup.py

config_parser.py:
    Create a parser for the config file.
    Extract the id_node, metrics require to be transmitted, interval in second on which the client will send a package to server.
    Extract the credentials for the pika connection
    CURRENTLY ALL PIKA CONNECTIONS ARE SET ON LOCALHOST AND THE AMPQ FIELDS FROM THE CONFIG FILE ARE NOT USED!!!!
    (but can be modifyed to use the ampq elements from the config file)


client.py:
    This module will create a pika connection to the server
    CURRENTLY THE PIKA CONNECTION IS MADE USING LOCALHOST, but ca be modified
    to use the credentials, and port for the CONFIG param which stored parsed
    info from the conf.ini file

    A collector is createad and metrics are collected. The collector is then transform
    to a json string and pass to the server DB

collector.py
    This class is responsible for collecting the required metrics given as an argumnt
    The metrics should be a list
    the collector package contains:
    -id_node as int
    -metrics collected as dict
    -time stamp
    will be created and send to the server based on the interval from the
    config file
    !!!Possible error if the interval is not given as a numerical value!!!(not tested)


conf.ini


test - folder containing:

    Tests for the config_parser:
        test for wrong filename
        missing ampq credentials
        missing CONF_MACHINE segment (responsible for identifing the current
        machine and metrics to be send)
    Test for the collector:
        test - require wrong or undefined metrics

    some conf files created for tests

Test result:
    passed



=============================================================
+server part
=============================================================

Files:

setup.py

api.py

    Recommmended to start only the apy
    IF YOU START THE API THE SERVER WILL START AS WELL

    It has a function for managing the default route, which will return a "about"-how to use the site; message displayed:
        "bonjour, request exmaple explained sitename/params?id_node=..." where id_node will be the id of the node that you want to receive metrics from

    It has a function for handling the route with /params
    This function will create a request from the DB for that specific node id, returning an array with packages (will return all packages with that id node)
    If the id_node isn't specified a message will be displayed


server.py

    The server will initialize the DB using ManageDb(api for db)
    It has a thread which will handle the pika connection with the client
    When a package is received the packet is stored in the DB.
    The pika connection is set with host='localhost', but can be modifyed in the future
    to use the prot, and credentials stored in config file, using the parser

    It also provides a function that can be called from the api.py called
    solve_request_from_api that will return a list of packages sotred in
    the db with the specified id_node (it returns all the packages stored
    with that id)


db-folder contains:

    ConfigParser_db:
        Parse the url from the config file for the DataBase

    model.py
        Create a model for the objects that will be stored in the table
        Table name is set as tableMetrics
        Contains class objTable which has:

            Fields:
                -id -(AS INTEGER) an id that will identify each stored package (unique)
                -id_node - (as INTEGER) id of the node that sent the package
                -metrics - AS A STRING
                -timeStamp - AS DATETIME - DEFAULT CURRENT DATETIME

            POSSIBLE ERRORS:
                the fields are predefined, so if the server tries to insert a package
                that has a different strucutre a error may apper

            Methods:
                to_dict - return the object as a dict
                save - save itself in the table, using a session as a param

    session.py

        Contains the Engine and a session for the DB
        A function that can initialize the engine and make a session

        Function ensure_session takes as param a function, and it ensures a new session
        for that function (if the session is not specified in the params list)

    manageDB.py

        Is an api for the DB
        This module creates the table which will store the packages, base on the url specified in the conf file

        add_pack() -> add a package to the db (the package is recived as a param,
        the session is optional, if not specified it will be initialize using ensure_session function from the session.py)

        get_pack() -> returns a list containg all packages with a specified id_node
        (the id is recived as a param,
        the session is optional, if not specified it will be initialize using ensure_session function from the session.py)

Test-folder contains:

    test_db_add_pack -> test add function for an incomming package
    if the pack isn't in the correct format or if, for example, instead of an int as id_node is passed a str an exception should be raised

    test_config_parser_server

Test results:
    passed

Flake8 test passed excep for:
    A unused function in client.py -> the function is there for a future update of the code

UTILS:
    contains default config files

Scripts for autoinstalling all modules needed and for creating default config fils
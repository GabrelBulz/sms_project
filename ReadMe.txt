
=============================================================
+Client_sms part
=============================================================

Files:

setup.py

ConfigParser.py:
    Create a parser for the config file.
    Extract the id_node, metrics require to be transmitted, interval in second on which the client will send a package to server.
    Extract the credentials for the pika connection
    CURRENTLY ALL PIKA CONNECTIONS ARE SET ON LOCALHOST AND THE AMPQ FIELDS FROM THE CONFIG FILE ARE NOT USE!!!!
    (but can be modifyed to use the ampq elements from the config file)


client.py:
    This module will create a pika connection to the server
    CURRENTLY THE PIKA CONNECTION IS MADE USING LOCALHOSt, but ca be modified
    to use the credentials, and port for the CONFIG param which stored parsed
    info from the conf.ini file

    A package containing the
    -id_node
    -metrics collected
    -time stamp
    will be created and send to the server based on the interval from the
    config file
    !!!Possible error if the interval is not given as a numerical value!!!(not tested)


conf.ini


test - folder containing:

    Tests for the ConfigParser:
        test for wrong filename
        missing ampq credentials
        missing CONF_MACHINE segment (responsible for identifing the current
        machine and metrics to be send)

Test result:
    passed



=============================================================
+server part
=============================================================

Files:

api.py

    Recommmended to start only yhe apy
    IF YOU START THE API THE SERVER WILL START AS WELL

    It has a function for managin the default route, which will return a "about"-how to use the site; message displayed:
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
    solve_Request_from_api that will return a list of packages sotred in
    the db with the specified id_node (it returns all the packages stored
    with that id)


db-folder contains:

    ConfigParser_db:
        Parse the url from the config file for the DataBase

    Model.py
        Create a model for the objects that will be stored in the table
        Table name is set as tableMetrics
        Contains class objTable which has:

            Fields:
                -id -(AS INTEGER) an id that will identify each stored package (unique)
                -id_node - (as INTEGER) id of the node that sent the package
                -metrics - AS A STRING
                -timeStamp - AS DATETIME - DEFAULT CURRENT DATETIME

            POSSIBLE ERRORS:
                because the fields are predefined if the server tries to insert a package
                that has a different strucutre ex:string as a id_node, it will fail

            Methods:
                to_dict - return the object as a dict
                save - save itself in the table, using a session as a param

    Session.py

        Contains the Engine and a session for the DB
        A function that can initialize the engine and make a session

        Function ensure_session takes as param a function, and it ensures a new session
        for that function (if the session is not specified in the params list)

    ManageDB.py

        Is an api for the DB
        This module creates the table which will store the packages, base on the url specified in the conf file

        add_pack() -> add a package to the db (the package is recived as a param,
        the session is optional, if not specified it will be initialize using ensure_session function from the session.py)

        get_pack() -> returns a list containg all packages with a specified id_node
        (the id is recived as a param,
        the session is optional, if not specified it will be initialize using ensure_session function from the session.py)

    Test-folder ........................TO BE ADDED


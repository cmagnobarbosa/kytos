==================
Auth Documentation
==================

The authentication module (kytos.core.authentication) is a resource under development that provides a means of protection for REST endpoints. By using this resource, endpoints that are public by default, now require an authorization token to be accessed.
 
All the authentication, token generation and configuration process is handled through the REST endpoints that are made available by default on kytos installation:

.. code-block:: python

 POST /api/kytos/auth/v1/users/ - This endpoint creates new users.
 
 $ curl -X POST \
    -H 'Content-Type: application/json' \
    -d '{"username":"kytos", "password":"youshallnotpass", "email": 
 "babel42@email.com"}' \
    URL


.. code-block:: python

 GET /api/kytos/auth/v1/login/ - This endpoint verifies a user and returns a valid token if authentication is correct.

 $ curl -X GET \
    -H 'Accept:application/json' \
    -H 'Authorization:Basic username:password' \
    URL


.. code-block :: python

 GET /api/kytos/auth/v1/users/ - This endpoint lists the registered users.
 
 $ curl -X GET \
    -H 'Accept:application/json' \
    -H 'Authorization: Bearer ${TOKEN}' \
    URL


.. code-block :: python

 GET /api/kytos/auth/v1/users/<user_id>/ - This endpoint gets details about a specific user.
 
 $ curl -X GET \
    -H 'Content-type:application/json' \
    -H 'Accept:application/json' \
    -H 'Authorization: Bearer ${TOKEN}' \
    -d '{"user_id":"001"}' \
    URL

.. code-block :: python

 DELETE /api/kytos/auth/v1/users/<user_id>/ - This endpoint deletes a specific user.
 
 $ curl -X DELETE \
    -H 'Content-type:application/json' \
    -H 'Accept:application/json' \
    -H 'Authorization: Bearer ${TOKEN}' \
    -d '{"user_id":"001"}' \
    URL

.. code-block :: python

 PATCH /api/kytos/auth/v1/users/<user_id>/ - This endpoint update a specific user.
 
 $ curl -X PATCH \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer ${TOKEN}' \
    -d '{"user_id":"001"}' \
    URL


The process to protect an endpoint is found in session `How to protect a NApp REST endpoint <https://github.com/cmagnobarbosa/kytos/blob/master/docs/developer/creating_a_napp.rst>`_
.


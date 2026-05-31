# Scrappy Pre Dev 01 Overview
For this first implemntation, in order to grasp how this project will flow, I had set up this project using simple heuristic by comparing words and complexity. This is very simple so I removed it to set up the router to take a request and compare it to previous requests to see which path is best for this project. So the first cycle was 
Request -> Router -> Check if complex Keywords -> decide model -> output toy response
Set up basic foundtion and though process for 
Request -> Router -> embed request -> compare and calucate cosine similarity -> decide -> output toy reponse 

# Scrappy Architecture Pre Dev 01

```text
                +----------------+
                |     User       |
                +-------+--------+
                        |
                        v
                +----------------+
                |    main.py     |
                |  CLI Interface |
                +-------+--------+
                        |
                        v
                +----------------+
                | route_query()  |
                |   Router       |
                +---+--------+---+
                    |        |
         Local Task |        | Complex Task
                    |        |
                    v        v

        +----------------+  +----------------+
        |   local.py     |  |   remote.py    |
        | Local Models   |  | Remote Models  |
        +-------+--------+  +-------+--------+
                |                   |
                +---------+---------+
                          |
                          v
                  +---------------+
                  |   Response    |
                  +-------+-------+
                          |
                          v
                       User

Current Components
Component	Purpose
main.py	        CLI entry point and interaction loop
router.py	Decides whether a query is local or remote
local.py	Runs local model inference
remote.py	Runs remote/cloud model inference
embed.py	Future embedding/vector functionality
documentation/	Project docs and development logs
Current Goal

Build a working routing layer that can:

Accept user input
Classify request complexity
Route to local or remote models
Return responses through a single interface

Next Planned Evolution
Embedding system in order to compare responses for route path


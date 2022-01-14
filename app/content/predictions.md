# Predictions

As with any new project, there are a few assumptions that must be made up front. Given the academic nature of a capstone, it only seemed prudent to adopt the hypothesis/results framework in the form of predictions and review. As such, this section will contain a collection of pre-development assumptions and decisions that have been made. With the completion of each portion of the project, the respective predictions section will be revisited and evaluated for accuracy. These musings on the expectations versus reality will be found in appropriately named sections in the [_review_](#review) section. 

## High Level Assumptions
One of the big decisions with this project early on was the micro-service architecture which is heavily coupled with the container first build strategy. On this side of the development path, there seem to be 3 major server-side domains: User Authentication, WebRTC relay, and realtime database subscriptions. While these could have been built in a monolithic fashion, one of the large goals of the project is modularity. Ideally, this should be a system which can be integrated selectively into other efforts within the lab. Regardless of the opinionated design found within each component, they should present a clear list of input and output parameters allowing for isolated use in other projects. For example, the User/Key Auth API component should contain all the necessary inputs and outputs to create users, create keys, authenticate users and keys, and provide permission evaluation for actions defined within the admin panel. While all of these features are being built specifically for this project, in isolation they could easily be dropped into a different project in the lab with just a little bit of legwork. Likewise, by splitting these large concepts into what are effectively a collection of smaller projects, it makes the work needed to be done far less daunting. 

Going container first was a decision made to alleviate concerns around deployment. A potentially large amount of software packages and libraries will be needed in order to effectively develop this project. As the list grew, the potential for pain during deployment only seemed to increase. For that reason, containers were chosen as a development tool to help enable the simplification of the development environment.  Through the use of Dockerfile's [^DFDef] to automate the environment setup of each component, and Docker Compose [^DCDef] to orchestrate their creation and destruction. Compose was was chosen over Kubernetes in interest of staying true to KISS [^KISS] in some aspect of this already complicated structure. Allowing for the easy attachment of system volumes and mapping of ports for web exposure, Compose provides just enough functionality to get the job done without adding the currently unnecessary overhead of dynamic load balancing and resiliency. 

That being said, this architectural decision doesn't come without drawbacks, to list a few:
* Everything is a web app, meaning error handling needs to be replicated across each component
* Transit lag is being introduced. An operation may now take 2 hops (1 to auth, the next to realtime db for example) before it can return. As opposed to 1 request to a single endpoint which then handles all the work with no external calls needed
* Specs need to be rock solid before development begins. Since each component will need to communicate with each other other web requests, the input/output documentation will need to be up to date and comprehensive in order to achieve proper communication between components. 

The duplication of work will definitely be a potential issue, the question still stands as to how much of an issue it will become. That can only be answered after development has begun.

## Component Level Assumptions
For each component, there are a few different assumptions being made which have guided their design. These can be in the form of language selection, off-the-shelf versus roll-your-own decisions, and feature set definitions. To better see what the project looks like at both ends, these assumptions are being listed here.

### Alert functionality implementation with a Realtime Database
For the alert functionality, we've opted to utilize a realtime database to implement this feature to cut down on development time. Originally, this was going to be accomplished with a web socket based design, which would open and subscribe all active users to a message queue on the server. This would allow the management interface (this is the demo site in this project) to publish messages to this queue which would be propagated to all clients. This feature started originally with the plan to use [Google's Firebase](https://firebase.google.com/use-cases), however it was quickly decided that the system should be able to function properly in a closed LAN environment with no access to the larger web. Upon the discovery of [Supabase](https://supabase.com), an open source Firebase alternative with self-hosting potential, the feature's implementation was migrated back to a Realtime database from its' brief foray with web sockets.

At time of writing, seeing as how Supabase implements an HTTP api with realtime subscription, the implementation seems rather straight forward. A very simple Flask API will sit alongside the Supabase container. All the API will do is act as a `start_session()` endpoint, which receives and session key and ensures that a table exists in the Suppose service for said session. If it does not, it creates one. Upon creation or validation of existence, it will return a 200 code and then client will then connect to the `ALERTS` table with the provided API and session key, and listen for new messages to be published.

### User Auth and Key API
The authentication API is primarily focused on solving the issue of differentiating between streaming sessions in the event that multiple users are active at the same time. To do so, it will implement a simple API Key system which allows developers to register an account and then request API keys. These keys will be stored alongside the unity client during the compilation process, and used to access the Alert and Stream services. Alongside the API Key issuing functionality, it will also contain endpoints for authenticating keys and creating new `Session` objects. These `Session` objects will act as references to each time a client activates a streaming session. This allows for a timestamped log showing everything an individual Unity client began streaming back to the server. 

This allows for 2 features, one for potential future development and another that we get for free right away. The free one, is that it allows for the querying of all past messages that were sent to a unity client. 

Imagining a scenario in which this system is integrated into a training application, in which a user works their way through a task in a a VR headset and an instructor follows along from a webpage. The instructor may offer advice to the user in the form of session alerts, by sending messages from their webpage. As a way to track progress, one could go back and see the types of messages that were sent from the instructor to the student, by requesting a collection of corresponding session keys and querying the alert database for all messages with a reference to said key. 

For future development, a recording feature could be implemented into the _Stream_ service which would allow for the capture of a WebRTC stream from a client for future viewing. This captured output could be referenced to the `Session` object which would allow for future querying.

For the implementation of this API, Django and Django Rest Framework were selected as the platform for development. Django is a web framework implemented in python, which follows the python ideology of being "batteries included", meaning it ships with substantial functionality that other frameworks may ignore. The particular functionality we're interested in is the fully featured User model. By using Django as a base, we won't need to implement any of the common requirements of a user model such as session tracking, password management, permissioning, and many other useful features. Not only will we be able to use this for the actual User model, but it is anticipated that these features can also be inherited into an API Key class to save development time.

That being said, Python is commonly discounted as a "slow" language due to its interpreted nature and lack of true multithreading. However, since Django is the framework powering applications as large as Instagram [^Insta] and many multithreading WSGI servers capable of serving Django applications such as [Gunicorn](https://gunicorn.com) exist, I believe that losses in speed are more than made up for by the returns drive by faster development cycles.

### Streaming Service
As for the WebRTC Streaming service, the biggest up front assumption being made is the network architecture for the stream relay. While we could have opted to use WebRTC as it was originally intended, in a peer to peer fashion, potential VR headset resource limitations became a concern. For example, both projects in which this will be integrated run on the Oculus Quest, a standalone VR headset powered by an android phone processor. While streaming to 1 to 5 peers may not be too exhaustive, as the number of active viewers rises the potential for visual degradation due to resource limitation rises. For that reason, the server will implement an SFU [^SFU] architecture, which will accept a stream from a headset, and then duplicate it for any viewer. This offloads stream duplication workload from the headset allowing for lower resource utilization, and potentially higher quality streams as a result of only needing to transmit it once.

### Unity Package
The Unity Package has the potential to require a very small amount of development time. This is due to Unity's inclusion of WebRTC capabilities within the engines standard library. For that reason, this portion of the project will effectively be a wrapper task, in which I will create a collection of scripts which use Unity's WebRTC libraries to stream to our desired endpoints. For that reason, a lot of time is planned on creating a simple developer experience for integrating this package into their project. I plan to create a series of UI panels which provide clear information on what information goes where, where to store the API Key, and how to ensure that the library is functioning. That being said, none of those features are guaranteed, and will be very quickly dropped as requirements if the usage of Unity's WebRTC library does not go as planned.

### Demonstration Site
This will be a very simple, bare bones, HTML webpage which allows a user to enter an API Key and see any streams which are active underneath said key. There will also be an input box which allows messages to be sent to connected clients. Seeing as how this webpage should be able to be written in HTML, CSS, and vanilla JS, without the use of any external framework like Angular or React, the anticipated outcome is that development is relatively short. The site will be hosted behind the larger Nginx proxy running the application, so deployment will be a couple of lines in the Nginx config and a docker mount command to place the files at `/usr/nginx/share/html`. 

## Tabular Predictions
Presented below are two tables, one being an estimation of the difficulty of each element and the other being a rough week by week timeline of planned milestones. 

### Confidence Estimations

| Project Component | Estimated Difficulty | Confidence in estimate | Confidence in ability to build to spec |
|-------------------|----------------------|------------------------|----------------------------------------|
| Realtime Database | Easy - 1 week        | 90%                    | 100%                                   |
| User/Key API      | Medium - 3 Weeks     | 75%                    | 90%                                    |
| WebRTC Server     | Hard - 5 weeks       | 90%                    | 80% (SFU v. P2P)                       |
| Unity Client      | Hard - 3 weeks       | 95%                    | 90%                                    |
| Web Client        | Easy - 1.5 Weeks     | 100%                   | 100%                                   |


### Planned Development Timeline

| __Date__ | __Milestone__                                                          |
|----------|------------------------------------------------------------------------|
| 01/14/22 | Git repository created and directory structure established             |
| 01/21/22 | Supabase + Postgres containers created and added to git                |
| 01/28/22 | Base Django project created in repo                                    |
| 02/04/22 | User Auth + html pages for browser access to API created               |
| 02/11/22 | API Key + all endpoints added to API                                   |
| 02/18/22 | Base WebRTC service in repo + Simple Unity Test Client                 |
| 02/25/22 | Basic WebRTC endpoints functioning with Unity Test Client              |
| 03/04/22 | SFU Architecture implemented in WebRTC Client                           |
| 03/11/22 | API Key validation logic implemented in WebRTC Client                  |
| 03/18/22 | WebRTC Component complete (Extra week left for flex time if needed)    |
| 03/25/22 | Base Unity client created and in repo                                  |
| 04/01/22 | Demo environment created and WebRTC attachment script created          |
| 04/08/22 | Alert script created and UI panels for framework. UnityPackage in repo |
| 04/15/22 | Basic web client frame created and hosting set up                      |
| 04/22/22 | Basic Web client complete. Begin E2E Testing                           |
| 04/29/22 | E2E Testing Complete                                                   |
| 05/03/22 | Capstone Defense                                                       |



+----------------------------------------------------------------------------------------+
| EARLY PREDICTIONS TABLE                                                                |
+----------------------------------------------------------------------------------------+
|                         |                      | Confidence   | Confidence in ability  |
| Project Component       | Estimated Difficulty | in estimate  | to build to spec       |
+-------------------------+----------------------+--------------+------------------------+
| Realtime Database       | Easy - 1 week        | 90%          | 100%                   |
+-------------------------+----------------------+--------------+------------------------+
| User/Key API            | Medium - 3 Weeks     | 75%          | 90%                    |
+-------------------------+----------------------+--------------+------------------------+
| WebRTC Server           | Hard - 5 weeks       | 90%          | 80% (SFU v. P2P)       |
+-------------------------+----------------------+--------------+------------------------+
| Unity Client            | Hard - 3 weeks       | 95%          | 90%                    |
+-------------------------+----------------------+--------------+------------------------+
| Web Client              | Easy - 1.5 Weeks     | 100%         | 100%                   |
+-------------------------+----------------------+--------------+------------------------+






+----------------------------------------------------------------------------------------+
| __Targeted Documentation and Paper Timeline__                                          |
+-------------+--------------------------------------------------------------------------+
| __Date__    | __Milestone__                                                            |
+-------------+--------------------------------------------------------------------------+
| 01/14/22    | _Predictions_ section written for project                                |
+-------------+--------------------------------------------------------------------------+
| 01/21/22    | Rewritten Introduction. Test cases written for user + key API. proposal  |
+-------------+--------------------------------------------------------------------------+
| 01/28/22    | UML Diagram created for user + key api. Proposal pitch rewrite           |
+-------------+--------------------------------------------------------------------------+
| 02/04/22    | Updated _proposal_ section with plans for user + key api                 |
+-------------+--------------------------------------------------------------------------+
| 02/11/22    | Write test cases/proposal for WebRTC service. Begin _background_ rewrite |
+----------------------------------------------------------------------------------------+
| 02/18/22    | UML Diagram for WebRTC Service. Continue on _background_ rewrite         |
+-------------+--------------------------------------------------------------------------+
| 02/25/22    | Prettify input/output document and add to paper. Complete _background_   |
+-------------+--------------------------------------------------------------------------+
| 03/04/22    | Flesh out remaining _proposal_ pieces (Unity + Web Page)                 |
+-------------+--------------------------------------------------------------------------+
| 03/11/22    | Complete _proposal_. Test cases for Unity and Web Page                   |
+-------------+--------------------------------------------------------------------------+
| 03/18/22    | UML Diagrams for Unity + Website. Write test cases for E2E Testing       |
+-------------+--------------------------------------------------------------------------+
| 03/25/22    | Begin work on _results_ section with already complete portions           |
+-------------+--------------------------------------------------------------------------+
| 04/01/22    | Flesh out _documentation_ section with completed UML Diagrams            |
+-------------+--------------------------------------------------------------------------+
| 04/08/22    | Add WebRTC results to _results_ section                                  |
+-------------+--------------------------------------------------------------------------+
| 04/15/22    | Write developer minded _Setup and Use_ documentation                     |
+-------------+--------------------------------------------------------------------------+
| 04/22/22    | Add basic web page results to _results_ section                          |
+-------------+--------------------------------------------------------------------------+
| 04/29/22    | Complete _conclusion_ and _abstract_                                     |
+-------------+--------------------------------------------------------------------------+




[^KISS]: _Keep It Simple Stupid_ https://en.wikipedia.org/wiki/KISS_principle#In_software_development
[^DFDef]: Docker can build images automatically by reading the instructions from a Dockerfile. A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image https://docs.docker.com/engine/reference/builder/
[^DCDef]: Compose is a tool for defining and running multi-container Docker applications https://docs.docker.com/compose/
[^Insta]: https://instagram-engineering.com/web-service-efficiency-at-instagram-with-python-4976d078e366
[^SFU]: Selective Forwarding Unit https://webrtcglossary.com/sfu/


# Proposal

## Pitch

To address the lack of platform agnostic solutions to the remote viewing
problem mentioned previously, I'm proposing a two part framework aiming
to provide plug-and-play access to a WebRTC stream from a Unity client,
as well as a communication channel for the synchronous transfer of
information back and forth. Piece 1 will consist of a Unity package with
simple configuration parameters to allow for a connection to be made
back to the web service. This Unity package will contain scripts to
attach to an in-scene camera as well as a blank gameobject to act as
hooks for the WebRTC and Messaging system. Piece 2 will be a web service
with a microservice based architecture, capable of providing 4 specific
services: User management, realtime messaging, WebRTC relay, and a
simple web client to interface with the entire system. For more specific
details, a feature list is provided below. This chapter will begin by
laying out a specification for each individual component. Following that
a list of proposed acceptance criteria for these components as well a
timeline for their delivery is provided. As the project timeline allows,
the goal is for each piece of the framework to be written as a
respectful citizen for each given platform (Unity, Django, etc).
However, this stretch goal is liable to be dropped if it threatens the
potential for deliverables to be completed by their prescribed deadline.
As deliverables are provided and components are finalized, the prototype
chapter will contain in-depth documentation.

**Features:**

-   A plug and play unity packages that attaches to a camera in scene
    and instantiates a game object which will provide a listener hook to
    be alerted if any new messages come through.

-   Simple Unity Inspector panel based configuration forms for easy
    setup

-   A Restful, Django based web api which ties into the Django User
    System

-   An API Key based permissioning system that allows unity game clients
    to connect to the web service without any additional login
    information

-   A WebRTC media server to act as a p2p relay for all transmitted
    video. Should leave hooks in for media manipulation as well as
    capture.

-   A Realtime Database (Open Source Supabase)[^1] for message
    broadcasting

-   A simple web application for testing that allows for the displaying
    of a unity client and a text box for sending messages to said client

## The Whys

A lot of decisions have been made early on which at first glance may
seem questionable, it's important that some justification is given for
them out front.

### Why Python? (and Django??)

-   This is a system built for work done in the lab. In the past, the
    primary point of hire is shortly after completing CSC231. As of
    2021, CSC131 and CSC231 are taught in Python. Since it is useful to
    get early insight on whether a new candidate has strong long term
    potential, having a system built in a language they're comfortable
    with will reduce the onboarding time it takes to assign them their
    first task.

-   Python is batteries included and has a huge developer community.
    From an efficiency standpoint, writing this in golang, .Net, C, or
    really any other compiled language would most likely show strong
    improvements. However for a minimum viable product, python would be
    the fasted language to iterate in and try new things out.

-   Django is an established framework powering sites as large as
    instagram.com[^2], it is also what we've been using in the lab for
    the past 2 years. It does come with a learning curve, but similiar
    to python itself also includes a lot of niceties that makes writing
    web applications easier. Add in the fantastic Django-Rest-Framework
    library and the decision is easy.

### Why Microservices?

-   It enforces well documented inputs and outputs as well as behavious.
    Since microservices are supposed to communicate using external
    messaging formats as opposed to directly calling code, you're forced
    to be more fine-grained with your endpoints.

-   Since the inputs and outputs are well defined, and the services run
    independently, youre microservices stack can run on multiple
    languages, allowing you to select the best tool for the job.

-   It allows for easy upgrading. If we find that as the userbase grows,
    the WebRTC implementation in python isn't scaling well, as long as
    we honor the previous API spec we can drop in a new GoLang
    implementation with almost no downtime or rewrites of other services
    required.

### Why Docker?

-   Similiarity amongst environments. If the development takes place in
    the same base container as the production service, we can avoid
    potential environment issues later on.

-   Aids in scalability. If the services are written to run 1 per
    container, and we toss a load balancer in front of them, we can spin
    up as many containers as necessary to handle surges in traffic

-   Ease of setup. Utilizing Docker-Compose, we could easily spin up the
    entire sytem with a single command. Gone are the days of multiple
    startup sequences

## Unity Client Package

All things considered, the Unity components should be relatively
lightweight and easy to produce. For performance reasons, only essential
processing will take place on device with the rest being offloaded to
the web services. For that reason, the architecture of the unity
component should relatively simple. Most likely it will container two
heavy lifter scripts, a single script to handle system configuration in
the Unity Inspector, and potentially one final script to handle
coordination between tasks.

-   CameraManagement.cs: This will be the script attaching to the
    desired in-game camera we'd like to stream. It will heavily utilize
    the experimental Unity-WebRTC package [^3]. This package is in an
    early beta state, with Android support (what we build to for VR
    executables) being recently released. I anticipate some potential
    debugging work during this portion of the project, since support was
    so recently rolled out.

-   AlertManagement.cs: This will be the script attached to a prefab
    which provides a listener hook for in-game alerts from the message
    broadcasting portion of our web service. At runtime, utilizing the
    (tentative) api-key based connection scheme, the script will send a
    request to our realtime-db that it would like to subscribe. Once the
    subscription is granted, it will listen for any new data and store
    it in a buffer for the developer to pull from.

-   InspectorConfigurationPanel.cs: This will be a script which will
    render a new Inspector pane on import \[sample photo here\]. This
    panel will allow users to easily input necessary information such as
    api keys, web service urls, and other important configuration data.

-   Coordinator.cs: If necessary, this will be a script which manages
    the runtime syncing of all three components mentioned above. If the
    scripts themselves start to feel bloated, this offers an easy
    offloading point to jump to. It would simply maintain references to
    each script individually, provide those references when necessary,
    and log all error messages.

## Web Service

### User Management API

The user management portion of the project will handle the creation of a
new user, authentication of API keys, and validation of active sessions.
It will contain endpoints for creating a new user, authenticating a
user, creating an api key, and listing all active api keys. Seeing as
this is a rest API, it will only serve data over JSON, meaning the web
client will be responsible for displaying this information.

Additionally, When the Media or Alert server receive a new API key, they
will first check to see if said API key is legitimate. If so, they will
then check their internal system to see if a service is already active
associated with this key, if not they will start one and then register
this new session with the User management API. The media and alert
servers should also notify the UserManagementAPI when the last user
disconnects from the session, so that the session can be marked as
inactive in the database.

![Current ERD as of Nov 19. 2021](assets/UserManagementERD.png){width="textwidth"}

### WebRTC Media Server

The WebRTC media server is being used as opposed to a traditional p2p
architecture for future features. While they are not within the scope of
the project, tiling multiple streams into a single view as well as
recording active streams, are both future goals that would require the
use of a media relay server. In this implementation, the media server
will contain an endpoint that listens for a WebRTC initalization
request, user type (streamer or viewer), and an APIKey. It will then
authenticate the key with the user management API, and then either
capture or relay the stream depending upon the user type. To begin, this
is planned to be implemented in Python using the aiortc library[^4], if
problems are encountered with latency or efficiencey, the fall back plan
is an implementation in either .NET or Go.

### Realtime Database

The Alert system has been the most dynamic part of this design. Moving
from websockets to firebase, back to websockets, and now landing on an
open source implementation of firebase. Supabase is an open source
realtime database engine built atop PostgreSQL. For this project, we'll
utilize it to provide a 2-way synchronous channel for messaging between
the web and unity client. For demonstration purposes, this will be
artifically locked to 1 way (web client -\> unity clients) but could be
turned into a 2way implementation with very trivial code changes. The
primary reason it will not be, is that defining a system for textual
user input in VR could be a capstone entirely on it's own.

::: framed
A sample definition of valid data

-   'alert', 'informational'

-   
:::

### Web Client

The web client has a few actions it needs to perform. First, it should
allows users to signup for a new account and generate an api key.
Second, it should allow users to see a list of all their api keys.
Third, and most importantly, it should allows users to see any active
streams and send a message to the unity clients which are curretnly
streaming. For demo purposes, I aim to have a single page similiar to
below that will allow a user to see what the VR headset is displaying
and send messages which are delivered to the user in VR.

![Example of potential interface for Web
Client](assets/WebClientMockup.png){width="50%"}

### \[MAYBE\] Load Balancing

ToDo: Touch on how this would be implemented and why. Need to decide
whether apps can be scaled horizontally by a generic orchestration
software like kubernetes, or if it should be a bespoke piece directing
traffic and scaling.

## Minimum Viable Product

In this section I want to define the acceptance criteria for the
project. Simple, objective components and features that need to exist in
order for this prototype to be considered complete.

## Testing

In this section I want to run through how I plan to test the system. Due
to time constraints, I think a real world stress test will be difficult.
Some of the automated testing I want to include could look like:

-   Stress test of the realtime database by spinning up a number of
    artificial connections

-   Stress test of WebRTC media server by throwing different
    combinations of synthetic clients and streamers at it

-   Usability test of the unity package. Give the package and a blank
    project to a few different developers in the lab and have them rate
    it's documentation and ease-of-user

## Future Work

In this section I want to lay out some of the future work that could
occur after the MVP is done. This most likely will not be accomplishable
in the timeline of this capstone, but may explain some of the design
decisions made throughout the process.

-   WebRTC: The ability to capture multiple streams from different
    clients and compile them into a single stream for viewing (4 unique
    camera views converted into a 2x2 stream)

-   WebRTC/RealtimeDB: The ability to add additional information atop
    the API key in order to differentiate different sessions within a
    single organization (Using this in a VASC type set up, allow
    multiple classes to occur concurrently but have the headsets stream
    to the correct teacher's portal as opposed to all in one big stream)

-   Web API: Modularity, try to abstract as much of the Django App's
    code away and pull needed information from the
    applications.settings.py file. This is standard practice for
    developing a django app with the intent of it being used in other
    projects. Will make this more usable.

-   All: Scalability. Short term plans entail writing the applications
    in a way that they are able to scale well on their own. If time
    permits, I'd like to explore how to scale them horizontally as well.
    It would be nice to have a single instance on a large server that
    can scale up and down as needed

-   : All: Packaging. For the purposes of the capstone this needs to
    work reliably on once machine, it would be nice to package it well
    though with documentation so that it is easy to adopt or deploy on
    your own machine.

## Deliverables and Timelines

In roughly 2 sentences per component, define what the deliverable state
of each one is. Alongside this, define large scale deliverables (i.e
WebAPI and Media Server acknowledge each others existence). With this, a
timeline of when these deliverables can be expected, as well as when the
large scale testing will occur. Ideally each deliverable will ship with
inbuilt testing, but for the purposes of finishing on time I'd like to
define a feature freeze date after which the project will cease to be
expanded and only be tested and refactored as necessary until the
capstone defense date.

## Diagrams, ERDS, Mockups, and More

This whole section is basically intended to capture any other important
diagrams or documentations that will help explain the project.

[^1]: https://supabase.com

[^2]: https://instagram-engineering.com/web-service-efficiency-at-instagram-with-python-4976d078e366

[^3]: see
    https://docs.unity3d.com/Packages/com.unity.webrtc\@2.4/manual/index.html

[^4]: https://github.com/aiortc/aiortc

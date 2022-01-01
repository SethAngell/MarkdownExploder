# Introduction

Mixed Reality has been slowly creeeping it's way into our modern lives
over the course of the past decade or so, with instances such as Pokemon
Go garnering half a billion downloads as of 2017. But unique virtual
experiences aren't the only potential benefit of this new domain. A
French study found that by integrating experiences similiar to the
Pokemon Go application, allowed students to connect more deeply with the
subject they were currently studying [@remmer_why_2017]. The potential
for use in education seems to be large, but that will not be the only
area where VR, and more broadly Mixed Reality, make an impact. Meta's
(previously Facebook) recent announcment and support of the Metaverse
concept seems to imply that big money is slowly but surely making it's
way into this field [@metaverse]. As with any expanding domain, there
will always be issues that need to be ironed out. \[need some sort of
pivot here into next topic\] In a vein similiar to how computers used to
take up entire rooms and can now be smaller than a stick of gum, game
development has only become more accessible to the average person as
time has gone on. Gone are the days where 3D game development required
construction of a bespoke physics engine, or a shader library. With the
advent of software suites such as Unity3D or the Unreal Engine, the
average consumer can build a 3D experience on the same technology that
powers Fortnite. But not only is this fantastic news for game
developers, but with the advent of affordable, consumer ready head
mounted displays, these same tools can be used to create immersive 3D
experiences of any sort. Be it educational, informational, directly
applicable to a business problem, or just for the sake of art. Theres
not greater example of this than the work happening in UNCW's Mixed
Reality labs right now. Utilizing the Unity3D engine and an assortment
of headsets, the lab has put out simulations to educate athletes on the
effects of heat strokes, teach children miles away from the coast about
sea turtles, and help government agencies gain insight on how better
analyze their data. But through all of these projects (most of which are
still in active development) a reoccuring theme has popped up. While VR
is an amazing experience, oftentimes there is a lot happening outside of
the headset that needs to get in. Alongside that, usually there are
interested parties who would like to know what is happening in
realitime. While there are platform specfic solutions, we've yet to
crack a one-size-fits-all solution to allow the outside world a looking
glass into what's happening behind the VR goggles. That is what this
proposal sets out to create. [\[needs a lot more info from below, as
well as citations. Also not sure I love the flow or this content as an
introduction in general. Will revisit later\]]{style="color: blue"}

1.  Open with information about how VR is a rapidly expanding field,
    which has also been around for quite some time

    -   Pull in something regarding Meta/Metaverse/Oculus (which is eww
        but also proof that this is definitely a mainstream topic now)

    -   Pull in info about how old VR is

    -   Touch on how VR usually involves a fully enclosed head mounted
        display (HMD), also touch on recent transition from tethered, to
        wireless, to fully on device

2.  Briefly touch on Unity3D (also the competitor I can't think of rn)
    and how they have made game dev so accessible

    -   How easy it is to get started

3.  Do a touch and go on personal background with this topic as an
    opener for short pitch

    -   VASC and ORNL

    -   How this problem keeps coming up

    -   Technical limitations

4.  Pitch on my problem statement: how do we manage multiple users in a
    single space effectively?

    -   Don't want to use platform solutions as they lock you into a
        system + security concerns

    -   Already usually utilizing some sort of webserver to offload
        processing

    -   Session monitoring platform

        -   Provides scaffolding for two important communication
            channels

        -   We already have Web Requests, this adds WebRTC +
            Websockets/RealTimeDB

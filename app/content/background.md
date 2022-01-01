# Background

## VR Development outside of games

There a few ideas going into this that I'll be considering table stakes
from here on out. In order to do so, I want to sell you on why you
should trust me moving forward that these are actually good ideas that
make life easier, and not unnecessary additional complexity. So lets do
a fun day-in-the-life of a non-game oriented vr developer.

### Game Development In 2021

While major studios are still building their own engines, a large market
share of the gaming industry is built atop of one of two engines:
Unity3D or Unreal Engine (maybe cite?). Now these are effectively
feature complete systems, coming out of the box with physics engines,
lighting libraries, sounds design tools, and a ton more. In the case of
Unity3D, which we'll focus on heavily the rest of this work, it also
includes a fully functional C#/.NET scripting backend for all logic.

-   Opinonated out of necessity

-   large emphasis on game stability

-   Built entirely around the concept of coroutines, allowing for larger
    more computationally complex actions to take place while still
    delivering 60+ frames a second

-   Requires a specific type of mental model for development. You ask
    the engine for things and wait on a response. Kernel-esque
    relationship.

-   Short touch on Entity-Component system, just a useful background
    thought to know when we get into the proposal

### Virtual Reality Development

Lots of stuff to cover here that will be used as justification later

-   Toolkit hell. Up until recently, unless you were a larger company
    who could justify multiple dev teams, you were more or less married
    to a headset. This is because you'd each headset came with a
    specific SDK for interacting with it, referred to as a . These
    toolkits would handle everything from button mapping, all the way up
    to the entire interaction system.

-   First with the Mixed Reality Toolkit, then eventually Unity XR, you
    gained the ability to target one toolkit which deployed to multiple
    different headsets. A much needed level of abstraction.

**Headsets:** Skipping over pre-consumer headsets and jumping right to
circa 2016, vr headsets have made a ton of advancements. Focusing just
on the lab:

1.  First you have the Oculus Rift, HTC Vive era in which you are tied
    into a beefy computer and the headset is effectively operating as a
    monitor. You're surrounded by 'lighthouses' which use infrared light
    to track your movements in the physical space and translate them to
    the virtual space. So long cable running off your head into
    computer, and IR lights in the corner of the room. Large setup.

2.  We start to see some wireless work done, vive puts out of wirless
    mod for their headsets that uses a PCIE card attached to another IR
    camera and an antenna wired directly into the headset. no more long
    cable tether, but headsets are still effectively monitors. Still
    need lighthouses

3.  Slightly coinceded with the wireless work, but we see headsets such
    as the vive cosmos which featured the computer tether, but also
    included on headset sensors that could track movement in physical
    space. Doing away with the requirement of the lighthouses.

4.  We have the modern headset that has taken the market by storm, the
    oculus quest. Running off the same Qualcomm Snapdragon processor we
    commonly see in Android smartphones, the quest is a fully contained
    VR unit. It doesn't require tethering to a computer, nor does it
    need lighthouses or other external sensors to help position itself
    in physical space. The quest is an all-in-one VR package that can be
    tossed in a backpack. Very appealing

## UNCW's Mixed Reality Lab

It be remiss to try and explain this project without background on the
two projects in specific which inspire. As mentioned previously, the
Mixed Reality Lab has it's hands in a lot of pots, but in an interesting
turn of events there are some shocking similiarities between very
different projects.

### Oak Ridge National Labs Data Visualization Project

Circa 2019, the group began working on a collaboritve effort with Oak
Ridge National Labs (ORNL) to produce a number of demonstrations as to
how virtual reality could help data analysts better interpret
information they receive. The pitched scenario varied depending on the
season, sometimes the idea could be that they only had a few minutes
with a hard drive, or maybe they were revisiting data they had
previosly. Also what if they were working as a team on a huge collection
if info that needed to be parsed through versus individually. Throughout
all of these demos, there was a constant wishlist item that has yet to
be completed. That is the request that there be some sort of real time
collaborative aspect to the simulations, so that indivudals outside of
the analysts office could see what is happening and get involved
themselves. This request, while interesting, has not yet been satisfied
due to a couple of blockers.

Firstly, however it is implimented it needs to be incredibly efficient.
Through multiple iterations, the project has always included some aspect
of photo analysis. This chews up lots of computing power in order to
process the images at runtime, and has led to a number of crafty data
structures to help handle the influx of work.

Secondly, the system needs to be secure. The sponsors of the project
envision it being used with potentially sensitive information. For that
reason, any system that is routed through 3rd party servers is an
instant decline.

Together, these two blockers have represented a signifigant hurdle to
completing a longheld priority.

### Virtual Access To STEM Careers

Another project of interest is the Virtual Access To STEM Careers (VASC)
initative, being completed in collaboartion with UNCW's Watson College
of Education. The larger simulation involves a narrative style VR
experience in which users learn about how to identify different types of
turtle tracks and the activities that wildlife conservation groups
perform to help keep sea turtles safe. In its' completed state, the
project is meant to be used in a classroom environment as part of the
science curriculum.

When imagining the deployment process of this system into the real
world, the topic of classroom managment quickly popped up. Primarily,
when you imagine working with younger children, being able to see what
they are seeing can help keep student's on track as well as guide them
through the activity and any problems they may encounter. While this
could be accomplished by plucking a headset of a student's head to see
what they see, the tempermental calibration and adjustment process that
takes place when putting on a headset would make this action a bit of a
timesink. For that reason, I high priority item of interest is some sort
of teacher portal which would allow instructors to see what their
students are seeing, in realitime.

## Literature Review

I've read a good amount of technical literature on how to accomplish a
lot of my goals, but not as much academic. I have some papers on my
reading list, but there are still some holes that I need to fill in.
Part of that will be more academic insight into the technology behind
the system (primarily looking at networking theory in relation to the
WebRTC 1 to many architecture). While I've grokked a good amount of the
implementation details, there are some efficiency and technical holes
that still need to be filled. That being said:

-   Pulled good information from the WebRTC book. Will want to do a
    little summary here of a paragraph or two on high level information
    that will be useful [@WEBRTC]

-   Sticking to the theme of a good O'Reilly book, I've been investing
    some concepts such as messaging queues and architectural patterns
    from this book. Will probably condense some of my notes into a
    summary here [@designing; @data; @intensive]

-   Useful networking considerations in the paper regarding remote
    rendering for vr. Not sure how much network testing I'll be able to
    accomplish, so this is a useful backdrop.
    [@kelkkanen_synchronous_2021]

-   I've read a few different engineering blogs from companies like
    Twitch and Discord who are working in a similiar problem domain, I
    anticipate a section about that research as well

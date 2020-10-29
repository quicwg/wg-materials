# QUIC 2020-10-22 Interim Meeting Minutes

Scribes: Robin Marx, Eric Kinnear

Recording available [here](https://youtu.be/p-ArboToDmk).

## Administrivia (10 min)

- Scribes, Blue Sheets, Note Well
- Purpose of the meeting
  - To understand the requirements for supporting additional multipath
    capabilities for QUIC beyond what is offered by the current version

Lars Eggert provides an overview of what QUICv1 can do in terms of Connection
Migration and failover and what the difference is to using multiple paths at the
same time

## MASQUE cross pollination (10 min)
[Slides](https://github.com/quicwg/wg-materials/blob/master/interim-20-10/MASQUE.pdf)

**David Schinazi:** Here to explain what MASQUE is and how it might be relevant.
HTTP supports CONNECT, works for TCP, not UDP. We need new ways to proxy UDP,
especially over HTTP/3 where UDP won't be encapsulated in a TCP stream.

MASQUE is new IETF working group to focus specifically on proxying over HTTP/3
Multipath and discovery are out of scope for MASQUE. They can still work well
together, since some use cases might require both multipath and proxying.

Three new proxying modes: (all have their own IETF draft documents):

1. CONNECT-UDP: like CONNECT but for UDP. Use QUIC extension DATAGRAM frames to
   prevent duplicate congestion control/loss recovery
2. CONNECT-IP: do VPN services over HTTP/3
3. QUIC-aware CONNECT-UDP: in order to avoid double encryption

Multipath:

- First example: using multiple paths between client and MASQUE proxy. This is
  orthogonal to MASQUE itself though (e.g., end-to-end could be HTTP/2 over TLS
  via HTTP CONNECT), no need for adjustments to MASQUE.
- Second example: end-to-end multipath: one path via MASQUE proxy, one path
  direct to the server (e.g., 1 trusted network + 1 untrusted network used at
  the same time). This is also orthogonal to MASQUE.

Main takeaway: MASQUE doesn't need to be multipath aware, no changes needed, but
can support some use cases.

#### Q&A

**Spencer Dawkins:** Thanks for the presentation. Do you have a sense of where
the question that came up during the adoption call for the IP-CONNECT, whether
that's leaning more towards an IP address or an IP prefix?

**David:** We will resolve in WG as part of adopted IP requirements draft. No
consensus on this yet. Can you file an issue in MASQUE for this to make sure we
discuss this?

**Spencer:** Yes

**Christian Huitema:** You say multipath and MASQUE are orthogonal, but they
interact via Path MTU. Any app running over proxy or VPN will have to do Path
MTU. Multipath means having separate MTUs over paths. Is this considered in
MASQUE?

**David:** My personal view is that that's orthogonal to MASQUE, that's specific
to QUIC, even without MASQUE and no Multipath, I still need to do Path MTU to
figure out how many bytes I can fit on the WiFi interface. Migrating to cellular
means I need to do Path MTU Discovery to figure out how that interface is
working, MASQUE and multipath don't change that.

**Christian:** If you do PMTUD in QUIC, we do this per-path. But if you do this
on the aggregate, then QUIC will have a hard time dealing with that. Either we
need to actively support this in MASQUE or not.

**David:** That also applies to IP, since your route could change without your
knowledge. That's not as likely though as it might flap more often if you're
doing migration. Potentially best to wait to see if that's a real problem in
real life, but let's discuss in the MASQUE WG. You could make an extension that
would notify of changes and request PMTUD to be re-done.

**Jana Iyengar:** Thanks for the presentation. One question: what you've shown
here is that MASQUE can use multipath and that they can coexist. Why would
MASQUE need multipath? What's driving the value here, in terms of use cases? Do
those use cases benefit from MASQUE?

**Lars:** We didn't ask David to present because he thought MASQUE would benefit
from Multipath, just because there are synergies

**David:** I'm personally not yet convinced that MASQUE would be measurably
better with multipath, but some of the upcoming presentations will talk about
the use cases there, and some of those use cases could involve MASQUE.

**Jana:** Ok, I had the wrong frame in my head for this presentation then. Lars:
Lots of the following use cases use QUIC as a tunnel, so that's why we wanted to
have this in here.

### Roberto Peon's Comments

**Roberto:** Sorry to rearrange agenda, but have to leave in half an hour and
wanted to get some comments in.

Why is the connection the right place for multipath? Historically we've chosen
it because:

1. We don't want to change a bunch of applications and require them to be aware
   all the time.
2. Connection has just evolved to be proxy for the "session" that the
   application is trying to do

Opportunity to rethink this now as well. Looking at reluctance from people to
use multipath when it does exist/ work, it is because we are burying it as
something opaque.

Example: If I am to do video, it is one of those obvious cases where using the
bandwidth from multiple paths will be useful. However, if I am worried about
rebuffering, if I want to make sure that the video doesn't stutter, I need to do
that while keeping the risks in mind. If I can't adjust or see the multipath
that's happening underneath, and that means that I might not be able to ensure
that it does the behavior that I need.

I might be better off if I, as the application, establish a session with the
server and control this myself. You could still put that behind a connection and
abstract it out that way, but it's potentially more likely to work for
real-world use cases.

Good to think about if we're putting multipath in the right place, it's about
muxing and demuxing, just now for paths. Do we want that to be associated with a
connection or somewhere else.


## Use cases and requirements (60 min)

### Multipath in Chromium (Fan Yang/Jana Iyengar, 5+5 min)
[Slides](https://github.com/quicwg/wg-materials/blob/master/interim-20-10/Multipath%20in%20Chromium.pdf)

**Jana:** Goal: Talk about experience going through Multipath with Google QUIC

**Fan Yang:** I work in Google's QUIC team, did a bunch of multipath work with
Jana and Ian back in 2016.

Before IETF QUIC, so gQUIC doesn't have multiple CIDs, so used Path IDs,
multiple packet number space. Unified ACK frame, contains packets received on
all the paths, assume that ACKs come back on fastest path. Separate loss
detection/congestion control per path. Retransmissions can take any path, not
just the original.

Moving data to a different path during retransmissions was very difficult, had a
complicated data structure, especially for packets that were on more than one
path. This should now be easier in newer implementation setup. ACKs look at
stream data, no longer individual packets.

For scheduling, put multipath in the connection, but need to know what the
application wanted. Example: minimal latency vs. bandwidth, causes us to use
lowest latency vs. both paths. Some applications care about data usage, so those
need to prefer WiFi. Some things are more sensitive to packet loss (e.g.,
audio), so for those you could use redundancy (duplicates across paths).
Difficult to have a single scheduling logic for all application types.

Inside Google, never got buy-in to develop a scheduler, nobody had a requirement
for multipath. Why not do migration first and see if that's working well enough?

Lessons learned:

1. Multipath is complex in terms of code
2. Scheduling is hard and needs to be driven by the application
3. Connection migration is typically enough for most use cases Example: Was
   sufficient for Google Search app, they're happy with the results and they
   haven't asked for multipath.

#### Q&A

**Spencer:** Think you're saying the same as Roberto: the more you know about
the use case, the more useful it will be: less interesting to have it as a
general purpose service.

**Fan:** Indeed, and so far that has not happened in practice that someone has
wanted to put in the work to do this

**Ryan Hamilton:** Quick question: do you think with the new architecture for
retransmissions being in the stream instead of being in the packets, would the
implementation be straightforward enough?

**Fan:** Totally, would simplify it a lot, no more connection between packets
that span multiple paths. The stream doesn't need to know, it either knows if
data has been acked and can be removed or if it needs to stick around.

**Igor Lubashev:** Talked to many internal Google client teams, but did you talk
to server teams if they were interested in Multipath? One example is YouTube.

**Fan:** Working on the server-side myself, we have a use case where the server
can use the preferred address after the handshake to move the client over to a
new place. That's _kind_ of multipath, but not really. To my knowledge, that did
not work gracefully with our infrastructure, so we shelved that for now and can
revisit later.

### Multipath transports at Apple (Christoph Paasch, 5+5 min)
[Slides](https://github.com/quicwg/wg-materials/blob/master/interim-20-10/Multipath%20transports%20at%20Apple.pdf)

**Christoph Paasch:** have been working on Multipath for a long time (e.g.,
MPTCP). Talk about use cases for them at Apple.

Use cases:

#### Siri (voice assistant)

7 years using MPTCP. Certain goals, very latency sensitive, want to get
responses to user requests as quickly as possible by minimizing latency,
especially at high percentiles.

Also want to reduce network errors, tricky because Siri is building up state on
the server as the user is speaking, when the connection is lost it's hard to
recover from that. Environment is thin bidirectional streams, so application is
sending small amounts of data in a very short time frame, server keeps
responding so not a bulk data transfer. Immediately bring up both WiFi and cell,
even for good WiFi we warm up the cellular link, allows immediately switching to
cell for sending or receiving, and have initial RTT measurement for both
interface types.

Exposed API for interactive, handover, aggregation modes for developers to use.
Siri uses interactive mode. Continuously checking which the most optimal path is
for a given packet (lowest RTT = best). Disparate paths between new data and
retransmissions, because retrans can block cwnd.

Requirements from QUIC:
- Continuous quality measurement
- Switch between paths more than once per-RTT sometimes, characteristics are
  changing on a very short time frame

#### Apple Music

Goal is to reduce playback stalls and their duration. Unidirectional bulk data
transfer for the entire song, playback buffer can mask networking issues.

Minimize cellular as much as possible here. Only when the music streaming is in
danger of losing quality/stalling, then transmit data on both paths. This is
using pooling to aggregate both paths.

#### Q&A

**David:** Thanks for the presentation, I think it's really nice to split things
out in terms of the use case vs. requirements on QUIC. Seems like most of the
requirements on QUIC are already covered by QUIC and connection migration. Do
you have an idea of things that require multipath? Apple Music and bonding could
need both, but that's the only one that I really saw.

**Christoph:** For Siri we switch paths at sub-RTT timescale, not sure that's
possible with QUICv1.

**David:** Trick is to validate both paths. Once that's done, you can migrate
continuously. It does have to be client-initiated, but from how I understand the
Apple use case, that is the case.

**Christoph:** If I can migrate between paths sub-RTT, then that's basically
resource pooling/multipath, no? Are we sure this is possible? Maybe, see
Christian Huitema's draft

**Lars:** Punt rest of discussion to the open discussion section.

**Matt Joras:** Does Apple have experience doing non-audio, e.g., video? Have
different considerations. Music is small, but modest video is already larger
than an entire song. Exacerbates policy problems that I've seen. Reducing
cellular data is noble, but that's not easy for something like the Facebook app
streaming video.

**Christoph:** We looked at video, one problem with adaptive bitrates, it's
estimating the bitrates that it's getting and we might confuse that estimation
with multipath. In terms of data usage, that is always a problem, the system
usually imposes restrictions on that. WiFi Assist on iOS, for example, limits
the amount of usage that can happen for cellular.

**Jana:** Useful to see where these things are being used. Siri switches at
sub-RTT timescales. Do you do this more than once per RTT? Imagine not, because
have to wait for feedback, so switch is probably just once per RTT?

**Christoph:** The highest rate is once per RTT of the lowest RTT subflow.

**Jana:** That makes sense. Does put a cap on how we think about resource
pooling here, because not switching at packet timescales.

**Jana:** About music: when you do pool, are you sending same data over multiple
paths (redundancy) or just maximizing bandwidth?

**Christoph:** We're trying to maximize the bandwidth, we use the scheduler in
one of the ICCRG drafts, it's a scheduler designed to optimize throughput.

### MPQUIC use cases (Yanmei/Yunfei, 5+5 min)
[Slides](https://github.com/quicwg/wg-materials/blob/master/interim-20-10/MPQUIC%20use%20cases.pdf)

**Yanmei Liu:** Present Alibaba use cases. They are already using MPQUIC at this
time.

#### UC 1 : New-retail e-commerce
Taobao mobile app: most popular shopping app in china. Shows short videos.
Already uses QUIC and H3 for streaming video. Also use multipath QUIC over WiFi
and 4/5G. Reducing stalling and rebuffering.

Customers are measurably more willing to buy products when they have the better
user experience, uploaders are more willing to upload when it goes faster.

#### UC 2: Taobao Live

Streamers streaming video to people watching what's happening, but they may have
a bad uplink. Uplink is sometimes very slow because it's done outdoors over bad
cellular. Use 2 uplinks from 2 different carriers simultaneously can help here.

#### UC 3: High speed rail in China

Train is going so fast that you handover between base stations every 13 seconds.
Can combine the cellular and train's WiFi at the same time. AliPay for online
shopping can be better as well for customers that are using apps on the road.

#### UC 4: 5G coverage

China currently rolling out 6GhZ 5G. Coverage is difficult due to higher freqs.
More coverage holes with the same base station density, 8% instead of
1.something% MPQUIC is a solution to this issue with in-app customization. (RM:
not sure what he means by this)

Scheduling is really important since we need to understand what the application
wants. We allow client/server interaction to give more information for that.

Show short video demo showing video streaming not stalling when done over MPQUIC

#### Q&A

**Lars:** Which MPQUIC do you mean? Draft-deconinck?

**Yanmei:** Generic MP-QUIC, not the specific draft

**Jana:** These are all using some form of Multipath capabilities. What's the
server? What's the client?

**Yanmei:** We deploy protocol both in our Alicloud CDN and client-side apps
like Taobao.

**Jana:** Are users actually using this? Or is this a demo?

**Yanmei:** Have a small-scale deployment and are experimenting with MPQUIC. But
it is running in production at this time for some of the users.

**Jana:** Have you experimented with connection migration in QUIC?

**Yanmei:** Yes. One issue is that sometimes bandwidth of connection is not
enough for e.g., Taobao live. Need multiple uplinks, making money when it's
stable and good. We do need bandwidth aggregation here.

**Yanmei:** Other use case is the high-speed train scenario. This is traveling
too fast for migration to keep up (migrate every 10s) in practice. On-board WiFi
is shared by too many people, so limited bandwidth on that path. Use that
together with per-device cellular is better for their customers.

**Jana:** Would love to see more details on what you are actually doing here,
since you're not doing draft-deconinck.

**Yanmei:** We have a draft with details:
[draft-an-multipath-quic-00](https://tools.ietf.org/html/draft-an-multipath-quic-00)

**David:** Was this end-to-end or with proxy?

**Yanmei:** End-to-end

**David:** Did you measure latency next to bandwidth?

**Yanmei:** Yes, just not shown in the slides.

**David:** Is MP making latency worse?

**Yanmei:** Depends on the area. Need to adjust schedulers to deal with this.

**David:** Agree. For some use cases all you care about is throughput, but for
others latency is important, so was just wondering what numbers you had.

### Satellite/terrestrial multipath communication (Jörg Deutschmann, 5+5min)
[Slides](https://github.com/quicwg/wg-materials/blob/master/interim-20-10/Satellite-terrestrial%20multipath%20communication.pdf)

**Jörg Deutschmann:** We have a use case to help with users that have poor
connectivity, terrestrial link for low latency and satellite link for high
bandwidth, but very high latency. With split TCP, we switch at sub-RTT levels,
but that's mostly because the latency is very high for the satellite links. Also
allow bandwidth aggregation of course.

With QUIC, there are no transparent TCP proxies anymore, so we have the
following requirements to meet our needs:

- Single-path QUIC over Satellite should work before it is used in a multipath
  scenario
- Need fine grained scheduling between links (sub-RTT). Would be good if ACKs
  are always on terrestrial links.
- Would like to use sat link ASAP, so using 0-RTT seems a good target for that

Have some lab-tests and are gathering results. Also thinking about general
architecture requirements for using QUIC over satellites.

See
[draft-deutschmann-sat-ter-multipath-00](https://tools.ietf.org/html/draft-deutschmann-sat-ter-multipath-00)
for more details

#### Q&A

**Matt Joras:** To clarify, for this use case this is essentially a proxying
tunnel use case where the end-user application is not aware of the tunnel.

**Jörg:** Correct

**Christian:** To clarify: is this deployed or research project?

**Jörg:** Outcome of research project. Starting field tests next year. Also
still need to setup tests with MPQUIC first. So this is early stage research.

### Hybrid access networks and requirements on MPQUIC (Olivier Bonaventure, 5+5 min)
[Slides](https://github.com/quicwg/wg-materials/blob/master/interim-20-10/Hybrid%20access%20networks%20and%20requirements%20on%20MPQUIC.pdf)

**Olivier Bonaventure:** Looking to present hybrid-access requirements on QUIC.
Use case: Hybrid-access routers, both DSL and LTE connectivity from a router,
can use either at the same time LTE is a backup. Sometimes you use LTE and DSL
both in rural areas where you don't otherwise have sufficient capabilities.

Already being done with MPTCP, which is deployed in practice. Typically combine
xDSL and LTE. End users use regular TCP with transparent proxy on the router
that proxies the connection so it becomes MPTCP to a specific proxy
(hybrid-access gateway) in the operator's network. That then speaks regular TCP
to the external servers. Similar to the ATSSS setups used in 5G (see later).

Main benefit is bandwidth aggregation. Congestion controller automatically finds
available network capacity. Network operators want to prioritize DSL over LTE
for costs. Path manager delays creation of LTE subflow if DSL link has room.
Packet scheduler prefers DSL if possible.

3 benefits:

1. By using datagram extension from QUIC, it's possible to provide bandwidth
   aggregation from non-TCP flows
2. MP-QUIC can aggregate bandwidth for different access links for different
   ISPs. Something about cloud.
3. MP-QUIC would be implemented in userspace so no kernel changes in access
   routers

On mobile devices, addresses and paths change over time, need to have a path
manager that can intelligently decide when to make and destroy subflows. Need to
have 2 or more paths, sometimes some will be preferred. Need to be able to
ping/CC/other ways to detect capacity and performance of the other paths.

MP-QUIC could have a solution where you don't need a proxy from the hybrid
access router so you can go end-to-end. Need the router to be able to tell the
device about the different accesses that are present. See also
[draft-ietf-rtgwg-enterprise-pa-multihoming-12](https://tools.ietf.org/html/draft-ietf-rtgwg-enterprise-pa-multihoming-12)

**Matt Joras:** Hypothetical question: If I am an end-application that's
natively using QUIC, would this setup (transparent to me) be able to tunnel my
connection over two paths without either me or the server knowing.

**Olivier:** Today if you use TCP, it would be transparent. If using QUIC, it's
probably going over just 1 of the 2 paths.

**Matt Joras:** And if I'm using QUIC with the MP-QUIC proxy, since datagrams
can be forwarded over both.

**Olivier:** Then you could send the QUIC DATAGRAMS as DATAGRAMS over the two
paths.

**Matt Joras:** That answers my question

**David:** Continuing from Matt's question: if sending on both, won't have
access on QUIC packet numbers. Reordering across paths could lead to perf
problems then. Have you deployed that?

**Olivier:** We've done some experiments with that, it works and there are other
ways that look at the timestamp to be able to reorder the QUIC packets or other
packets on the server side so that you can avoid having it cause problems.

**David:** So, artificially delay packets to put them back in order. We've seen
issues with this in TCP, haven't tried in QUIC.

**Olivier:** Depends on implementations. Looked at this a year ago, QUIC
implementations at the time were much worse at handling reordering than TCP
implementations, that may have changed.

### Multipath in 3GPP ATSSS (Spencer/Mirja/Florin/Hannu, 5+5min)
[Slides](https://github.com/quicwg/wg-materials/blob/master/interim-20-10/Multipath%20in%203GPP%20ATSSS.pdf)

**Spencer Dawkins:** No hats. Not talking about ATSSS itself but as a multipath
tech. It uses only 2 paths: one 3GPP and one non-3GPP. They have rules that
assign nodes per flow.

This presentation is combo of things in ATSSS and enhanced ATSSS. ATSSS is two
protocols, one using MPTCP, one using a separate setup without specific
protocol. For now they're doing steering and switching only for non-TCP. For
enhanced ATSSS they're looking to add support for splitting for non-TCP traffic.

They have proposed tunneling/proxying setups for this. When we say MPQUIC I'm
talking about general Multipath QUIC, not draft-deconinck.

First use case: campus/enterprise. Similar to hybrid access that Olivier
presented.

Already deployed ATSSS modes today:

- active standby -> only needs migration
- smallest delay -> only needs migration
- load balancing -> requires real multipath
- priority-based -> partially could use migration, needs multipath for other
  aspects

Some of these modes can work pretty well with Connection Migration in QUICv1,
some of them do require multiple paths to be used simultaneously.

All new steering modes in eATSSS require multipath; cannot be done using just
connection migration. For details, see slides.

Seems to be headed for a much more dynamic use of multipath paths for these use
cases. Hope they can use MPQUIC for this to build on QUIC stacks (no need to
have separate protocols deployed to, e.g., smartphones)

If we don't do something with QUIC, we'll be doing it some other way. Want to be
able to do in-order delivery of multiple paths that were sent over those paths
working at the same time.

#### Q&A


**Martin Duke:** I think what you're showing is customer QUIC packets
encapsulated in DATAGRAM frames of an outer QUIC connection?

**Spencer:** I think that's what it'll end up being. Martin: If that is indeed
the use case, why not just use layer 3 solution and switch QUIC packets over
multipath paths?

**Spencer:** If you back up to slide 3, the picture on that slide shows what's
currently deployed. One of those things is MPTCP and ATSSS-LL (a lower layer
solution that only supports steering and switching). I think they're trying to
reason from what they have now to where they should be going. I think it's fair
to say that this work is probably earlier in the process than you're going to
get from most SDOs, but 3GPP wanted to work closely with the IETF to avoid
duplication. Very interesting question, thank you.


**Mirja Kühlewind:** To clarify: what you describe is ATSSS lower layer, no
additional protocol. This lower layer only supports steering and switching.
Don't really want to use both paths simultaneously because that would lead to
heavy reordering, which has heavy impact, so they try to avoid this.

**Richard Bradbury:** What's the time-scale of this for 3GPP, Rel-17? That's
very soon.

**Spencer:** That is the current Plan of Record in 3GPP. I'm here to help the
IETF to get there.

**Mirja:** This is under discussion currently. Also discussion to move deadlines
by 6 months. They just need a working group draft, just need a clear view if
this is coming or not.

**Richard:** Don't need RFCs yet?

**Mirja:** Definitely not mature enough, but as soon as there's a WG document
that might be sufficient and they can move on.

**David:** Thank you for the presentation, especially the terminology, that
helped a lot. You described benefits of this project in terms of network paths
being used. (noises woo woo) What's the benefit to the user in your mind?

**Spencer:** This is the provider viewpoint. Many of the other presentations are
about the use cases the provider expects that people will be running over their
networks.

**David:** I'm not sure I understood, rephrase: This is good for the provider,
but without end user benefit?

**Spencer:** No, sorry, I'm saying that I'm presenting the provider view, which
assumes there are benefits for both the users and providers.

**David:** We assume the benefits exist,s but what exactly are they expected to
be? Why do we expect practically?

**Spencer:** Yes, those discussions happened in 3GPP a long time ago.

**David:** And we don't know the outcome of those conversations.

**Spencer:** They happened before I got there, I don't know

**Mirja:** The benefit you get is the direct interface between the UE and the
network, as well as that the proxy has info about what's happening on the
network, so more information about which path to use

**David:** Talking about end user here: what benefit do I get from this when
using my smartphone?

**Mirja:** You have two paths available if the server does Multipath, you could
do it end to end but you're missing information from the network about how those
different paths are working.

**David:** As a typical end user, what is the benefit to someone that is
non-technical?

**Mirja:** I think you are asking a question about how tech is put in the
tariffs?. If you can offload your traffic to managed WiFi network you get it for
free, but that's not a technical question.

**David:** So answer I'm getting is that this is useful for network operators,
but not necessarily for the end user.

**Hannu Flinck:** May I interrupt?

**Lars:** We've got to move on

## More use cases from Mike Bishop

**Mike Bishop:** Have been talking about scenario where clients make requests.
Those might end up at instances that do not have all information that the client
is requesting, so they have to recursively fetch those resources. It would be
nice if those nodes could directly send their replies to the client, instead of
routing through the original instance first. This is difficult now because of
packet number spaces, would be interesting with Multipath. Client would just see
this as a server with multiple IP addresses.

**Lars:** I believe that Nokia has IPR on this for Multipath TCP, I know that
because it's my patent.

## Open discussion (40 min)

**Lars:** Purpose of meeting was to get a feel for use cases and what is missing
in QUIC v1. Use the remaining 20 minutes to see what use cases if any could
already be supported with what v1 already offers. Second part would be which
other functionality we could add to v1 to support other use cases.

**Martin Duke:** I think migration is very close to solving many of these use
cases. Seeing a lot of fast switching back and forth between paths, while
current assumption in QUICv1 is that old path can be "thrown away", so we would
just need to fix that. Solidifies my view that we should not tackle scheduler
problems.

**Christian:** Roberto and Christoph both made a very good point that scheduling
needs to be done in the application. Need some sort of hot-standby scenario with
a simple algorithm, anything more complex -- Roberto is right, better to have
multiple connections with a lightweight management system and then the
application can do its own scheduling on those connections.

**Ian Swett:** Think we have drafts that already solve the Direct Server Return
case presented by Mike Bishop (last use case)

**Martin Thomson:** There are interesting interactions between application and
multipath. QUIC is maybe less susceptible to burying these things deep in the
OS, but want to up-level a bit. Question I want to ask is what the QUIC WG
should be working on next, rather than just if we should do Multipath. I am
convinced that there is value in MP, but don't think we'll get the sort of
synergies with deployed protocol is we allow the protocol to (...) and I don't
see people implementing QUIC at the moment interested in doing multipath

**Eric Kinnear:** Connection migration does not cover bandwidth aggregation for
both paths at the same time, this was intentional: could be added by a small
extension for people that want to experiment. Policy about money is a challenge
where you'd normally not want to use both an expensive and inexpensive interface
at the same time, but if you're on cellular and can use even-bad WiFi then you
might be more willing to do so when you'd otherwise be on cellular. This was new
to me, so thanks to people presenting that. Like Roberto/Martin, feel
applications need to be able to talk about best scheduling for performance,
system may know about policy choices. Most questions seem to be how to deal with
policy and platform design, not about how to build a protocol we can actually
deploy at this time.

**Mirja:** Just wanted to react to Roberto. I really disagree with his point of
view. Many benefits doing it on transport (e.g., retransmitting across paths).
Agree there is benefit from linking with app, but typically just a handful of
schedulers needed for some scenarios and app could just choose 1 of those
pre-defined schedulers. I think this is a general feature that smaller apps that
don't put effort into developing their own stacks could benefit from having
available in a simple way.

**Yunfei:** More of our experience with multipath QUIC, definitely agree that we
should keep things simple. On another side, based on our experience, if a
customer wants to use multipath it still needs additional capability. I think
the better way is to review all the proposal and see if there's a simple way to
see if we can enable that capability. Lots of the policy and scheduling needs to
be decided elsewhere anyways. On the money said, we do see charges for cellular
and WiFi are different and one way is for us to collaborate with mobile carriers
so that we know when the customer is using our app and then they can get free
cellular for our app's traffic.

**Jana:** On policy and scheduling I agree with Eric. Use of multiple paths is
tied closely to both network and application. Either make API really thin, or
make app decide, is just a question of where you draw the line. Fundamentally,
MP is tied deeply to its use case. This is what I was hoping would come through
in the presentations. But I feel application is super critical in figuring out
what MP really means. Another way of saying is that connection migration -is-
multipath. Use of multiple paths is what multipath is. What experience do we
have? Comes back to priorities and lack of experience and up-leveling this
conversation. I know multipath is valuable and interesting to work on. However,
given that QUIC already has a piece of Multipath. How much does that give us and
how much would we need to increase? I've got use cases and I don't know if the
signaling in QUICv1 connection migration is going to be sufficient for me yet.
This is unclear at this time. Would like more experience with connection
migration before deciding how to extend this further.

**David:** What I'm getting is two main use cases: Multipath to a proxy (ATSSS)
and multipath end-to-end. First, to the proxy, it sounds like there's no clear
benefit to end users, quote RFC8890 "the Internet is for end users", I don't
think QUIC is a good fit for ATSSS. If they're asking us to add complexity and
remove encryption, why are they using QUIC in the first place? What about GRE
and other (shout out to chat, make sure to like and subscribe) protocols.
Second, Think multipath could have value to the end user. But agree with Jana:
first need to prove this is better than Connection Migration. All of the data
that we've seen so far doesn't take into account connection migration, would
like to see that sooner.

**Kazuho Oku**: Wanted to make a small comment -- agree with Mirja that
transport can provide direct connection that the application can use, but that
approach has failed with HTTP/2 because the scheme is too complicated and too
few servers can do it well, better to do this in small steps before we can come
up with something general.

**Spencer:** Experimental was good enough for what I was hoping for from a
multipath QUIC. Is there anyone here for whom experimental is not good enough?
(no one said "yes")

**Olivier:** Re Roberto: I think it belongs in layer 4, because there we have
congestion control info and retransmission capabilities and those work together.

**Yunfei:** Connection migration + QUIC do better than LTE handover? Given that
for some extreme mobility use cases we think with MP-QUIC we can do better than
LTE handover.

_End of queue_

**Lars:** Thank you Robin and Eric for taking minutes. Seems clear we need to
talk more. Encourage using the mailing list rather than GitHub issues.

Always possible to have a second one of these sessions. Talk offline to see if
you can consolidate use cases moving forward

This is a hard problem, it's unclear what functionality is missing at the
moment, are the stacks that are large deployments even interested in deploying
this, what information does the QUIC stack need. With Multipath TCP, it was a 3
year EU funded research project, and then we got _started_ on the rest of the
deployment work. I would hope that we can find something that is small and can
enable experimentation that will enable maybe a subset of the use cases.
Hesitant to see us doing a full multipath architecture in a single goal.

Please use the mailing list, talk with folks, see if we need more discussion
time like this, see if we have agenda time at 109. Thank you all.

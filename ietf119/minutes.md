# IETF-118 QUIC WG meeting


## Tuesday, March 19, 2024

Scribe: David Schinazi, note-taking enthusiast

### Chair Updates

### qlog (Robin Marx)

Ted Hardie: Please email moq-chairs@ietf.org with what extension points you'd like.

Robin Marx: will do.

Lucas Pardue (as individual): We'd love to hear more from moq but overall we think the extensibility story is good enough and we can proceed even though moq isn't done

Robin: agree

## Multipath QUIC (Yanmei Lui, Mirja Kühlewind)

Kazuho Oku: This introduces a cost that I don't love but I'm ok with it. Plz merge

Alessandro Ghedine: Plz merge

Jana Iyengar: I haven't read the PR, but I like it

Magnuz Westerlund: Support merge

Christian Huitema: I didn't like this at first but now I do. Let's merge

Show of hands tool: should we merge the PR?
23 Yes, 3 No, 3 No Opinion

Lucas Pardue (as chair): plan to move forward with merge unless we see objections on list

Kazuho: propose to use static path IDs, see issue 321 opened yesterday

Mirja: let's discuss on issue

Issue 47: server-created paths

Kazuho: how critical is this?

Mirja: we've seen implementers get this wrong - this simplifies

Kazuho: what about server opening new paths?

Mirja: yes

Kazuho: propose to either not do this or punt

Mirja: it's not that much complexity

Christian: we need to do the odd/even split now because that can't be added as extension later. Potential compromise would be to only use even numbers for client for now, and reserve odd to do server-initiated later

Mirja: Love it, plz write PR

Christian: I've written it down

Magnus: MPTCP has this, we should have it to allow replacing MPTCP with MPQUIC. 3GPP likes MPTCP. This is also useful for P2P

Mirja: could we instead have server ask client to open path

Magnus: yes but would cause latency impact

Lucas (IC): +1 to Christian's compromise

Lucas (chair): support in chat for compromise

Mirja: we can punt for now and can always add later

Marten Seeman: this could be interesting for my NAT traversal proposal, I need to think about it

Ian Swett: We should do this, I have multiple use cases

Christian: Let's definitely put the even/odd split in the draft and go from there

Lucas (chair): Let's see a PR

Mirja: will do

Issue 295/313 retire CID on all paths
Christian: from implementation experience, explicit is better

Marten: prefer implicit

MT: are other resources cleaned up at the same time?

Mirja: yes, packet number space

MT: great, drop it all

Magnus: fine with implicit


### Ack Frequency (Mirja Kühlewind)

Issue 235

Jonathan Lennox: Instead of only looking at CE vs non-CE, should we look at any ECN change to detect bleaching?

Mirja: You want to know as early as possible

Lucas (as error code enthusiast): this doesn't really matter

Ian Swett: huge thanks to Mirja for doing all of this work, really improved the draft

Matt Joras: we will soon start the WGLLC (last last call)

### Resource exhaustion attacks on QUIC (Marten Seeman)

Martin Duke: this was already discussed in issue 3905

https://github.com/quicwg/base-drafts/issues/3509
We added SHOULDs and MAYs so maybe that's good enough?

Marten: we should provide guidance

Alessandro: this keeps happening, we'll have to keep updating RFCs all the time

Eric Kinnear: links are asymmetric, the congestion control situation here does happen in practice

David Schinazi: many things can cause this, suggest writing down guidance about never letting your stack buffer infinitely - this isn't specific to QUIC for that matter

Lucas: special thanks to everyone for handling the responsible disclosure process correctly here

### 5 min - QUIC on Streams (Kazuho Oku)

David Schinazi: I think this is actively harmful, it might weaken the deployment of QUIC and lead folks to deploy protocols over QUIC expecting performance properties that won't be met by TCP

Kazuho: Disagree, there's real value in limiting work duplication

Eric Kinnear: the number of networks that block QUIC isn't going down, this means accepting that instead of fighting it

Ian: this looks a lot like WebTransport over h2

Kazuho: problem is abstraction is not at correct layer

Marten: I like this so I wouldn't have to implement WebTransport over HTTP/2

Christian: the reason for blocking UDP is traffic inspection, those networks are likely to block QUIC over TCP

Martin Duke: concerned about https://xkcd.com/927/ otherwise I'd like to see performance numbers

Ted Hardie: interesting idea but current design is problematic: common API assuming QUIC underneath will be surprised. This pushes complexity up the stack into the application because of those differences

Yaroslav Rosomakho: 2 reasons for blocking QUIC (1) not knowing any better (2) inspection for security. This happened in WebSocket, but was resolved by having great applications that required WebSocket. Same here, get more applications going over QUIC - this will go against that

Cullen Jennings, David Schinazi enthusiast: this solves a short-term problem but will cause a long-term problem. Best long term plan is to use QUIC everywhere and let network security admins know that QUIC is great and has good connection-oriented properties so they should let is through. Future is longer than the past

Victor Vasiliev: WebTransport aims to provide the same API as QUIC. Our MoQ implementation works over both WebTransport and QUIC very easily. This draft is pretty much the same as WebTransport-over-h2

### 10 min - QUIC BDP frame (Gorry Fairhurst)

Marten: big fan of careful resume and saving congestion control information from one connection to the next. But I don't think it should be sent on the wire. It can be done locally to implementations inside tokens that are opaque to the peer. Sending this explicitly on the wire gets tricky because both endpoints can use different congestion controllers so the values could mean different things

Gorry: I don't think that's a concern

Ian: I'm not seeing a use case for this. The ones I have would be better solved by SCONEPRO

Matt (as individual): Gorry, is this specific to sending over the wire, or the more general concept of optimizing CC

Gorry: I don't care about particular solution, but care about the client sending explicit info to server about path changes

Lars Eggert: we tried this for TCP long ago. Sounded great in theory but caused serious issues in practice. QUIC codepoints are cheap. Please experiment first then tell us about it when it works.

Lucas (chair): this isn't a new topic, we get different signals each time. let's do a show of hands

Is the WG interested in adopting work in this space (this space meaning the explicit sending of CC info)
12 Yes, 13 No, 4 No Opinion

Ian Swett: maybe this should go to the new congestion control WG

### 5 min - FEC results (François Michel)

No time for questions

### 5 min - Accurate ECN

Ran out of time



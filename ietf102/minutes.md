
# QUIC Working Group Minutes

* *IETF102 - Montreal*
* *Scribe: Joe Lorenzo Hall*

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [QUIC update from Martin](#quic-update-from-martin)
- [Ian on Stream0](#ian-on-stream0)
- [Brian on Operational Drafts](#brian-on-operational-drafts)
  - [open issues (see slides)](#open-issues-see-slides)
- [Martin on Retry](#martin-on-retry)
  - [retry overview](#retry-overview)
  - [looping](#looping)
  - [spoofing](#spoofing)
  - [0RTT and Retry](#0rtt-and-retry)
- [Martin on Discarding Handshake keys](#martin-on-discarding-handshake-keys)
- [Martin on Stateless Reset](#martin-on-stateless-reset)
- [Mike B on CIDs](#mike-b-on-cids)
  - [Sequence without Gaps (-13)](#sequence-without-gaps--13)
- [Mike B on HTTP update](#mike-b-on-http-update)
- [Ian on Recovery](#ian-on-recovery)
- [The FUTURE!!!!](#the-future)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
## QUIC update from Martin

State of drafts (about 100 open issues): half editorial, parked, or v2

things we will not solve now are labeled with the v2 label in the issue tracker

many of the remaining are pretty close to done... and main reason that they are not done is that they take work

PLEASE HELP US CLOSE THESE BASTARDS!!!

Jana: many are still working on draft-12

hopefully by next intermin we'll be on -13

EKR: if you go to github there's a PR that has examples of ClientHello

Mnot: have a very active grop of imps. ~10 imps now. have been meeting regularly

have a Slack group for this

## Ian on Stream0

TLS records may span multiple segments of TCP

In Quick draft-12 (prior to Stream0), a bit more complicated

draft-13 uses "QUIC record layer design" squashes this down by one level

benefits of new approach, no dbl enc, path validation, QUIC doesn't need to know TLS handshake state

costs? new API for exposing TLS key schedule

another change... was issues in no having separate packet spaces.

by spoofing an unencrypted packet, you could create a hole that would fool sender into thinking their encrypted packet was delivered

benefits of separate packet number spaces: solves the shadowing attack, etc.

cost: structure costs... requred a sent_packets structure per enc level, must store an ACK structure per enc level during hs

QUIC transport retry... current retry complicates TLS interaction... requires over cleverness in TLS to preserve the handshake transcript

retry is not encrypted at all

uses toke to prove source address for 0RTT or Retry (used for both)

benefits: save CPU on server, don't have to touch a TLS stack or know TLS hs state

open issues (#1486, #1451): looping with retry packets, etc.

## Brian on Operational Drafts

IETF QUIC applicability: application des and mapping designers on use of quic

IETF QUIC manageability: application and network admins on the implications of QUIC deployment for common management tasks

applicability: basically no changes, just reved the draft to unexpire it.

goal: facilitiate design fo non-HTTP application bindings to QUIC

Not many changes here but little controversy, so little attention

manageability: surfaces the protocols' wire images present to devices on the path

goal: provide a guide to QUIC's wire image for operators/management vendors without making them read the whole transport spec

changes to -01: update headers, fix CIDs, encrypt PN, mention SNI for app identification, point to spin bit experiment for potential RTT

after a bit more work on load balancing/CID usage, this will be mostly done

### open issues (see slides)

moving forward with -applicability

editors can suggest text, but we may not be the best potential authors for some of this stuff

we currently address implementers, application-layer users, and deployers with -app, is this too much?

Jana: we talked about -app a while ago. Do you cover implementors?

there is some of that, seeds, etc. there is some stuff on what an error interface should look like.

Mirja: touches point about interface discussion. may want to say more about transport interface in the document

Gorry F: we should be careful as we write it that we write to the audience so that they'll read it. two groups of people you could write to

A: that's the -app / -manage split

Tommy P: this should describe all the bits that should be there to (something). He volunteers.

Ted Hardie: want to understand what you're proposing. Mnot, you're proposing that the publication of these drafts would be later than the other drafts?

That might cause pain... operational aspects coming later than protocol docs.

once we have sig. interop testing under our belt, people will start using these (they already are)

Mnot: but the docs could be better than they would if we take our time.

Mirja: I agree they should be published at the same time. even if you send it at the same time, that may not result in them being RFC'd at the same time.

Show of hands: who can work on one of these open issues. (A smattering of people.)

EKR on agenda bashing: would like to get Retry done... so much list traffic

(we'll try to get things done.)

## Martin on Retry

identified a whole bunch of issues here

### retry overview

Format: -13 is a mess...

not encrypted but includes a packet number that is encrypted?

proposal: don't include a length or packet number field

new weakness: can't coalesce Retry

proposal: don't worry about it

(no one at mic)

### looping

clients accept multiple retry packets... no way to distinguish different retries

proposed fix: non-terminal server MUST provide a dew CID

### spoofing

attacker can spoof a retry if they can see the Initial

attacker can also alter the CID

MitM can provide a Retry with its choice of CID and strip the toke from the subsequent Initial

Jana: are we saying that a server has to (something)?

only requirement here is that the values are unique across this particular exchange

(?): is this still keeping the same invariants

We're not going to be able to do that here.

The main reason we had invariants is to ship v2

if we're allowing anyone on a path to send a Retry, that may become an invariant

EKR: starting to think we went of the rails when we decided that OECID was the thing that correlated the request and response

we already have a random value packet... which we use all over the place.

There is a lot of stuff here we can work with.

MT: we discussed this on the Issue... for a few people having to remember the output from the encryption was hard.

Ok, but this is lame.

proposal: We already have a quasi-random value in the auth tag of the Initial.

We now have a bunch of new complexity... terminal/non-terminal. Some servers are going to be bouncing around alot.

MT: don't agree with that assessment.

You're assuming you know if you're terminal or non-terminal server.

MT: are you the only one that thinks this is a problem

Subodh Iyengar: why did we make a different decision to allow Retries to change the CID? If we bind these, this wouldn't be a problem.

Why don't we bind to CID?

MT: if you're going to open old issues that we've already litigated, no bueno

Ian S: I think this is find. Don't have an objection to EKR's approach.

This is a non-issue from an operational perspective

Tommy: agree with Ian, if we have a section that talks about the philosophy around what is CID and when to use it

Mirja: this is an open issue in the -applicability

MT: whatever that doc says the transport doc has to be coherent

(?): there were proposals to prevent spoofing involving putting stuff in the handshake

Nick: so, being able to use the tag assumes you have access to it

if you're using enc offload the client wouldn't have access to that.

The CID has a lot of direct easy access for these cases.

EKR: you need the tag /ciphertext for PID (PNE?)

If you offload all enc, it would pass down something different, you wouldn't have access to that

EKR: this is a consequence of not encrypting Retry.

Mike B: the retry that we have doesn't need to be version-independent

MT: we can decide to encrypt it, but the design team decided they didn't want this.

Jana: this was basically to be as close to (?) in order to do this cheaply

Martin D: if the point is (?)

EKR: it's not about saving bits, this is just not aesthetic

Suggestion that we validate choice of CIDs is a good one

Spoofing proposal: we can do nothing because we don't promise any protection for an attacker with these capabilities (during the hs)

EKR: (?)

MT: only attack aware of is attacker can chose CID that ultimately reaches the server (man-on-the-side)

EKR: requirements obviate off-path attackers (?)

MT: we made sure that you had to see the packets in order to attack... off-path isn't going to see that.

maybe we do nothing

Igor L: attacker with ability to see hs can target negotiation, pretty powerful

Jana: slightly different flavor of attack... allows a MiTM to direct all traffic to a different server

might want to discuss separately if we want to authenticate on CID

(?): there is an imp concern here... server can force client to always use the same CID

MT: right, if you force someone to use the same keys, ossified around a particular key

### 0RTT and Retry

what happens to your 0RTT after a Retry

one catch: unlikely that the keys used for 0RTT would change, so need to use new packet numbers

Subodh: could we say that if you get a Retry packet, the server says "I"m not committing to state anymore"?

MT: PR says that you should have to expect to resend them.

EKR: I like the analogy to TFL. also made some noise about how this should be a new connection, generate a new Client Hello, then you wouldn't have to screw around with packet headers

Patrick McM: raising this issue is great, love this in my code... not a 0RTT after a retry. one less RTT is still a win

Like a new packet number rule, consistent with rule that you don't retransmit packets

EKR: having people send packet number 0 and then 52 is not going to inspire a whole lot of confidence.

Mike B: the other reason we didn't reset, if the 0RTT packets were buffered or delays, they can be processed after your Initial

Can a serveer send Retry if it receives a 0RTT packet?

proposal for this: SHOULD NOT rather than MUST NOT

## Martin on Discarding Handshake keys

When can Keys be destroyed? (#1544)

Simple solution: timers

treat each packet number space separately

a space is kaput when both read and write keys for next space are ready

set a timer when done and destroy the keys when it expires

Alternative: HANDSHAKE_DONE frame

explicit signal, endpoints would destroy keying material on receipt

proposal: "You might want to clean up keys, you might want to use a timer for this"

Mike B: now that we have ext framework, we're looking for an extension to exercise it HANDSHAKE_DONE would be a fine extension.

David (Apple): let's keep this out of the main spec

Kazuho: people that prefer (?) can do (?), don't think we need this for that

Subodh: in the previous iteration, there was more interest in this but not with separate spaces

EKR: text needs to say that in a sequence the last packet you get is here. happy to provide text.

Patrick M: if infinite is ok, may need non-normative text that says that but talks about timers

## Martin on Stateless Reset

Problem: stateless reset is indistinguishable from a QUIC packet by design

... that no one can decrypt

can result in a wild loop/resend

simple solution: stateless reset is a small packet footprint... e.g., if too small to be a QUIC packet you'd drop it.

only send it if it was smaller than the packet that was received.

Slightly more complex solution: random drop sateless reset if it ins't smaller than the incoming packet

Gorry: can you be robust to this or not?

Channeling from Jabber: Praveen: makes it hard for predictability

Erik N: make sure that everything we have here is deterministic and fast.

MT: proposal is that if they do not decrease in size you drop?

Erik N: but there may be an encapsulation or translator that makes it bigger. Want something more explicit to terminate

Tommy: can an endpoint carry a decaying number of resets it's been handling... "in the past 10s I've sent a ridiculous number of resets, stop"

Jonathan Lennox: does it have to be that the packet is smaller than a stateless reset? or exactly the size?

EKR: these are optimizations

you have to keep some state or you can't keep track of crap that's coming in

simple solution seems ok, only getting small packets... any real app will send big packets

concur with Nick's point that randomization (?)

Ian: we do time-based dropping

This basically never happens unless it happens all the time.

very bimodal until all of your servers are DDOS each other

Had to solve for ClientHellow (?) and in that case we decremented the TTL

can copy the TTL (?)

Brain T: what Ian said

another thing you can do is tweaking the size of stateless reset... at most packet size - something (encoding TTL in the packet size)

Manasi Deval: If we compare this to TCP, there are some state machines that are triggered at connection termination

given the scale it's not just as easy as setting a timer.

Patrick M: we might want to jettison stateless reset altogether, but have been convinced that operationally can't work around this.

Jana: (?)

MT: I like the TTL suggestion, we can strongly recommend. IPTTL, that is.

## Mike B on CIDs

useful for helping connections survive changes to the four-tuple

some problems with sequencing with gaps (pre-PNE)

with PNE (packet number encryption) we can get rid of all of that gappy crap

use an unordered set... but to break linkability if your peer changes, you also need to change... how to you signal this.

We do need that seq number

EKR: not entirely clear to me that when peers change CID you need to change

you need to change CID when path is changed.

Spec recommends that you change CID when you think there may be a NAT change, etc.

If the peer responds with a CID from an old connection, linked

EKR: a behind a nat, b no behind a nat (a and b our peers)

in this case don't need to change CID

not yet persuaded to see if the path has changed

MT: we're being conservative, when a changes CID, they may want to appear to be c (so that it looks like someone else)

EKR: but, if you receive a new CID from someone who's address has not changed, it's not clear to me you need to change your CID.

MT: we chose the lock-step condition because it is convenient.

Mike B: this is background for how we got to where we are on -13

EKR: why can't you just have a rule that you update when your peer has a new transport address

Jana: I don't think you can assume that you only need to do this on path changes.

... continuing with the preso

### Sequence without Gaps (-13)

if you are starting a new path, you will have to send a CID that is higher than any one you've ever used.

This is essentially like a ratcheting

proposal: NEED_CONNECTION_ID frame, request to have at least X CIDs beyond seq number Y

RETIRE_CONNECTION_ID frame: declares old CID no longer associated with this connection

Kazuho: we need a design group for this.

## Mike B on HTTP update

EKR: the premise of QUIC is tight integration. Can live with this but don't like it.

Subodh: getting flow control is hard enough, don't want more edge cases...

Let's do ugly and make the layers match.

Please implement and find the rest of the potential problems.

## Ian on Recovery

some editorial issues, but want to get people thinking about non-editorial

early retransmit threshold is 1/4 or 1/8 (#945)

this is inconsistent... want to make both of them 1/8 until we have more data.

Gorry: isn't this related to cong control?

Jana: QUIC is using it's own mechanisms in Linux using TCP

Max Data Received before sending an ACK (#1428)

Reno used for cong control, but is ACK-clocked

proposal: sender sends a transport param indicating retransmittable bytes received before sending an ACK

(?): have you considered (?)

Ian: This isn't as much about appropriate byte content but timing.

Praveen: we just need an ACK if you've reprocessed two bytes (?)

## The FUTURE!!!!

Sept. interim planned in NYC. Registration closes in 3 weeks, please register.

will do an interop before hand as always, need to figure out the scope

We'll need a 8th target (we have a 7th)

MT: I propose the same one we had last time, things have changed in -13

please HTTP emphasis.

EKR: we did -13 plus 1498

MT: if we get the changes to Retry in, let's try that too.

We think we are close to done.

Should be able to ship on schedule.

Please start reviewing substance of docs, editorial not so useful at this point (save for later)

Going to be progressively harder to make a big change as we move down the road.

We are hoping to ship protocol and ops drafts together... have the invariants draft too.

Also on spin bit elephant in the room... need data an experience as to its usefulness in managing networks.

won't be delaying last call if we don't have this data

Brian T: we've taken the spin bit of the interim agenda, can we put it back since so many people using this are there

Mnot: anticipate spending a lot of time on Bangkok

May need an early 2019 interim, Jan/Feb... make arrangements but not pull the trigger until after Bangkok.

The name of QUIC itself still causes confusion, press users implementers

Google QUIC vs IETF QUIC

changing the name is not realistic

when we ship this thing we'll call it QUIC v2

if this gives you heartburn, talk to mnot and lars

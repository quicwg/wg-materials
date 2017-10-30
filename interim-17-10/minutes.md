# QUIC WG Interim Meeting Minutes

* Date: 5-6 October 2017
* Location: Seattle, Washington USA
* Host: F5
* Chairs: Lars & Mark
* Attendance: 49 registered locally, 15 remotely

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [4 October 2017](#4-october-2017)
  - [Interop Summary](#interop-summary)
  - [Architectural Issues](#architectural-issues)
    - [Silent Close](#silent-close)
    - [Connection close discussion](#connection-close-discussion)
    - [Idle timeout discussion](#idle-timeout-discussion)
    - [Stream Abstraction](#stream-abstraction)
      - [How to kill streams](#how-to-kill-streams)
    - [Unidirectional Streams](#unidirectional-streams)
- [5 October 2017](#5-october-2017)
  - [Architectural Issues (cont'd)](#architectural-issues-contd)
    - [ACK Frame](#ack-frame)
  - [Header Compression](#header-compression)
    - [Data on HOLB](#data-on-holb)
  - [Issue 693, AEAD Protection of Cleartext Packets](#issue-693-aead-protection-of-cleartext-packets)
  - [Next Steps](#next-steps)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## 4 October 2017

Adminsitrivia: Welcome, Blue Sheets (white today), Scribes, Note Well, and Agenda Bash as well as wifi pwds

Scribe: Sean Turner

### Interop Summary

We had a pile of implementations and we developed a matrix to do interop.  Got a fair level of interop for the basic stuff: connections, http.  Some on other issues.  Here's a list of the implementations:
 https://docs.google.com/spreadsheets/d/14Vw0EX8XG0YRKxSdcDxloBjOkTt9FpbJMpBAg1Hvbmc/edit#gid=0

The complete implementation list was updated.  It can be found here: https://github.com/quicwg/base-drafts/wiki/Implementations

Things that were issues:

* Flow control around stream zero data - bounced around a couple of ideas: e.g., exempt stream zero.  All of these are in [Issue 825](https://github.com/quicwg/base-drafts/issues/825).
* Whether 0 is a valid packet number.  It is valid and people know how to handle it.  Whether it 0 should be a valid number is up for debate.  See [issue 832](https://github.com/quicwg/base-drafts/issues/834).
* How should we encode connection ID integer or not specify.  We've converged on a hex string.
* Where the ACKs go for client clear text?
* Difficult to test some of the reject cases.  Need some wiki document to explain which port does what.
* There's a problem with the HTTP/0.9 specification. After the get is it a FIN or not?
* Working out the best way to float the logs around.  Lars and EKR offer web servers that allow the logs to be returned.
* HRR logic is maybe not what you think it is.

We started a slack it's not under note well.  It's just for talking about getting interop.  Issues need to be on the ietf mailing list.  If you'd like an invite ask anybody for one (e.g., chairs, EKR, mcmanus, etc.).

We're also starting to work on flow control, but we're not sure how to test it.

Toying with the idea of setting up some CI of all the implementations.  If you're interested contacted EKR.

Patrick: What's implementation draft02 targeted at for Singapore?

mnot: We'll talk tomorrow about that.

A set of test cases would help.

Christian: HTTP/0.9 was the default test, but it would be nice to have a list of files to be expected.

mnot: Need somebody to write that down and then use it.  Volunteer!!

mnot: Who's going to be in Singapore for the hackathon?

Answer: 15 or so.

05 and 06 drafts closed around 80 issues.  Need to confirm consensus.  Very few people read through the list.

Need a little more time to review this.

ACTION: 2 weeks to review the list.

### Architectural Issues

#### Silent Close

[Slides](https://github.com/quicwg/wg-materials/blob/master/interim-17-10/connection-close.pdf)

Slide 5 - Application Close

Details for this need to be added to the draft.  Obviously needs some discussion.

Question: How is this different from application-driven intermediate close.
Answer: The former is more of an abrupt error close, this is more graceful.

Connection close says this is fatal.  Application close is more graceful.
Could we rename immediate close to immediate reset?
This is an API issue unless we're talking proxies.

What happens at the transport level? What is the flow?

Christian: When writing the tests, developed an API that asked is there something still in transit?  Not hard to do.  If you have this then the application can use this. When everything is closed then it closes.

Jana: This is the other model.

EKR: How the transport behaves different in the existing scenario.  Imagine we didn't have the functionality we'd still have two of 'em so we're just adding an error or it's discarded.

Christian: At the transport layer it's ambiguous whether it's new data or a retransmit.

EKR: These's some queue from the application the transport that I'm done.

roni: There is a message between the applications and is there a transport message as well?
Jana: no

roni: need to specify the application message in each application document. What about max_data and max_stream data in the close_pending state?

Mike: It might be more useful to have what's in the HTTP spec as an example.

Jim: TCP has this interesting problem.  But, we need to think about the problem as opposed to jumping to the solution.

Christian: I think you are trying to solve an application problem with a transport mechanism. This might be a bad architectural choice.  Better if the application closes after it does the check pointing.

Preveen: Liked Jana's idea about close no error case.

Roberto: He read some stuff - get his text.  He's said he'd DROP IT HERE :)

Close semantics *for a protocol*:

* Application calls close() on the QUIC connection (not a stream).
  * Implementation can drain all buffers and then call CloseImmediate(NOERROR). For a single p2p connection, how is this different from:
* ApplicationClose, then draining? For a proxy, this seems interesting:
  * When it sees CloseImmediate, regardless of its forwarding state, the proxy should tear down all related connections/requests.  Whereas, when a proxy sees ApplicationClose, it should continue to service forward unforwarded data.
* Close semantics *for an API*. The API may distinguish between close and shutdown, e.g.:
  * Close: immediately tear down everything, stop all work
  * Shutdown: drain everything, then eventually stop all work and tear down.

*Break*

Martin: During the break, we came to some conclusions: in the application close case there are more cases than listed.  Subsequent to that, once the app has done this it writes all of this in to the buffers and the transport has all it needs to send.  Once it's done sending then it transitions into the draining period.  This is all fine.  Need to talk about how the shutdown process so how it includes all of the states.  We also concluded that the no error case is useful because if you operate a transport layer intermediary you hae an agreed shutdown via something at the transport layer ... the client says I'm done, servier says I'm done, but the intermediary just stopped and enter idle timer and this is bad.  The no error case is good.

Jana: Likes it - yeah!  Christian's point is maybe a way to model this.  If we're having the application negotiating anyway then they can negotiate fully.

Martin: Is not sure that it's not as important to standardize as some people think because it's a division of labor thing that's not visible on the wire.

EKR: The point Roberto made is that it's not nice to the middlebox when things just stop.  One way is to have a message that says I'm in draining another way is to have a message that says it's fine but I'm done.

Alan: One question: Can you gracefully terminate that streams that send no explicit signal.  yes

Alan: Please don't legislate the API - ie, agrees with Martin.

Peter: Agree with MT that most of the discussion has been about the division of labor is.  Better if we don't have to specify it.  But, the question is whether we need some extra message or whether we are changing the semantics of connection close.  Am I right in that assesment? Partially right.  If we pick a new state we need a message to signal the state change.

Victor: Confused about whether it's an API issue.  The API question is whether it blocks.

MB: Do we need an explicit signal.  Thinks Roberto's use case was pretty compelling. Do we have consensus on that.

Pinder: We need the state - no clear that we need a message.

Christian: Yes we can do a silent close but a message is nicer.

Jana: Would like to table it (ie come back to it)

Christian: If you want to manage this at the transport layer need a frame there to handle this.

Jim: Saying that we only have to wait one more one round trip is a bit naive.
(Note from Spencer as individual: I'm assuming that this is a heuristic, and wonder if we can do better than "pick a number", which I think is what Jim is saying here. But I didn't interrupt the discussion in the room to say that.)

WG consensus: none

Slide 6 - Draining Period

Jim: This is a good example to know what problem we're trying to solve.

preveen: Not sure these times are enough.  This is going to block the application if we get these wrong.

MT: These numbers are more of a suggestion.

Slide 7 - Idle Timeout

was silent close ;)

Slide 8 - Path Timeout

Ted: Want to make sure we can support mutli-path.

Jana/MT: yes that's one of the reasons for it.

Path timeout haiku was a hit.

break for lunch (1 hour)

*Scribes: Roberto Peon / Martin Duke*

MT: conclusions for changes: remove ACK from draining period; allow CONNECTION_CLOSE in response to CONNECTION_CLOSE to acknowledge it; send CONNECTION_CLOSE (NO_ERROR) in the case that the application has received, sent and received acknowledgements for everything.

#### Connection close discussion

Jana: Proxies make it difficult/require semantics to be clear w.r.t. flushing the data. As long as the close happens after all data ack'd, things are OK, but if not, then it gets tricky.

Bishop: The endpoint waiting for conn close needs to wait for the acks, but the acks are from the proxy. Thus, the proxy needs to change behavior based on error/no error.

Thomson: The problem is that ack's aren't end to end

Christian: Applications need to checkpoint

Jana: We do have idle timeout, expect this in the common case (conn idle for some period of time, then it goes away).

Bishop: App close comes mostly from servers that are shutting stuff down.

Jeff: Apache max-requests, as an example of server closing/terminating.

Closing connection to client different from closing connection to peer.

Jana/Jeff: Agreement that we want this semantic, want a different frame.

#### Idle timeout discussion

Jana asks: What did you think about the haiku?

Jeff asks that all proposals be in haiku: Jana counters that new proposals should be limericks

Martin Duke: Don't I want to run a timer from the last packet I've sent

Jana: Depends. Path timer should be in play when data is in flight, else idle timeout.

Krasic: Counter-intuitive that this happens for?

Thomson: Bad to have stream specific things for generic transport, perhaps other than stream 0
Restate principle driving this: Idle from the point that the app tries to use the conn. So, app wants to send, recv, or is doing ping.

Jana: valuable if these don't cover all use cases, if people send notes saying what is missing.

Igor: not sure about not running idle timer when path timer is running (or vice versa)

Martin, Jana: Timers are separate, up to implementations to decide how to deal with them/combine.
Worth some recommendations/suggestions

Praveen: Why so many timeouts, Why not let conns live forever.

Thomson: How long will you make the application wait?

Jana: Reason to have this in the transport is that the app won't know the moments in time where acks are sent/received. Timing is known to the transport. Transport could send the timing up , but may not.

Duke: Why not require pings to keep alive

Thomson: You could do this, e.g .with timers

Roberto: Ewwwww, no thanks.

Jana: There are also nat timeouts to deal with.

Dmitri: connections in TCP can last forever

Roberto: Most implementations tell you when the conn closes

Christian: Nat timeouts differ for TCP.

Eric: I already dealing with NAT timeouts, adding another that you can mess up. Idle timeout means I'm only willing to hold your state for X time.

Jana: Client may say: I have no idle timeout, or special case of 0.

Roberto: PINGs are evil, though a necessary evil.

Christian: Two timeouts: Check that path is still alive. Application layer timeout to check that the user is still interested. In that case, if the underlying transport keeps pinging, this is a poor result. Or we define the idle timeout as : We see traffic that implies that the application is progressing. The ping shouldn't count there.

Buck: Talking about keeping conns alive for a long time. The value of doing that should vanish with O-RTT.

Bishop: Main place to want a ping: Indicate something supposed to come back that could take a while. Form HTTP layer, when have open request, will also have a handle on transport to tell it to send pings to indicate activity/interest.

Jeff: Hanging get/push where I'm expecting data. Common case is notification channel

Christian: In that case, I think that there is no app-level timeout. Application is saying keep state because I want it forever that is fine. If you're doing a webserver because there may be a new request sometime in the future, then you want to kill it. An auto-ping wont do that. Cue from the fact that the application is sending.

Thomson: Application doesn't know that

Christian: The app can know that.
How do I differentiate from a hanging connection for notifications for a connection that is expecting a response immediately

Thomson: Christian's scheme can't differentiate these.

Christian: Depends on protocol

Jeff: Mostly gonna be HTTP, for good or ill

We're talking now about question: Is ping necessary in the idle connection?

Christian: Ping for MTU.

Praveen: There is different for ping for transport vs application

Christian: Ping is primarily for transport.

Jeff: As written, ping is transport with guidance from application.

Christian: can see sending ping for variety of reasons: Keep alive or other reasons. Appears to be transport machinery.

Jana: Also for connection migration/liveness checking

Roberto: PING in HTTP/2 served 2 purposes: keepalive and application reasons. Can we separate PING and timeout?

Duke: Is the impact of this discussion gonna impact the PR at all?

Jana: Yes

Thomson: currently ping is used for multiple purposes, some by transport, some by app.

Is the concern that ping will reset the application timer?

Flipped. The transport ping shouldn't reset the idle alarm. The idle alarm attempts to figure out if the application is idle or not.

Buck: If you care about the control stream fo rH2 you could close it/reopen. Nothing says you couldn't

Igor: Main point of the idle thing: Determine if other endpoint has gone away. Otherwise you could have an app that could send a ping and verify that the other side has went away, but this is possible problem for mobile.

If you fail to verify that the other side has gone away without sending a ping. Is this the only use case for app idle?

Mike: it isn't the other side going away it is about if the app is doing something or not.

Igor: This is up to the app. If not doing anything, it could close().

Jana: The reason to not move all of this up to the application is that you want to be careful about precise packet time.

Igor: Seems like the use case is to not wake up cell radio.

Thomson: Ignore other uses, for the application: It is a clear signal to the transport that it wants to use the connection. The reason we have ping now, without pending pull request, is for an explicit signal by the app to keep the connection alive.

Jana: If implementation says if you have streams open other than zero or one, then I'll send a ping is reasonable

Christian: Plenty of reasons to send ping outside of transport, e.g. tail-loss probe (TLP)

Jana: TLP isn't a ping

Jeff: using the stream state as a signal might be a cleaner signal

Jana: shouldn't specify that the transport should have open streams to send pings

Christian: DNS doesn't have special streams.

Praveen: One thing we're ignoring is that a long-running connection has opened its congestion window. The reconnect is different.

...Do the editors have enough info to iterate?

Martin,Jana: Yes.

#### Stream Abstraction

[Presentation](https://github.com/quicwg/wg-materials/blob/master/interim-17-10/stream-abstraction.pdf)

##### How to kill streams

Stream contains 2 data channels in opposite directions. Both sides FIN

Abrupt closes: RST_STREAM, STOP_SENDING

Stream Abort, <= -04: used to be that no more data send, retrans, no more read. requires matching RST_STREAM

Since -05: RST_STREAM says no data send/retrans, with offset for flow control

STOP SENDING says read no more data

Objection: half-resets are bad. keep it bidirectional to avoid TCP half-open issues

Objection: Stop-sending should be an application issue.

*pause presentation*

Roberto: HTTP is not the only use case. Video might adapt to a different bit rate, so STOP_SENDING might be useful.

Ian: would not a bidirectional RST be adequate?

Roberto: Should stop_Sending reset the stream or mandate a FIN (retransmit data or not?).

Christian: STOP_SENDING means "please reset"

Igor: What are the application semantics? "I am not reading" or "give me what you have buffered?"

Roberto: the transport implications are different?

Buck: Dash doesn't do that

Victor: Why isn't this an application construct?

Buck: video shouldn't decide mid-stream it doesn't want the object

Roberto: No, I can store video with different qualities, different segment size or different GOP size simultaneously and adapt between these. Larger segments have better quality per bit.

Buck: If you care about latency, you don't have that granularity.

Roberto: Disagree, but we'll take it offline

Jana: We should consider other use cases, yes

Bishop: Previously, there was a special error code for STOP_SENDING

Jana/Martin T: Disagreement over what GQUIC does historically

(I'll explain here: h2 RST_STREAM(NO_ERROR) is sent AFTER the response to say that you don't care about the request, but it is still killing both sides.  There is no special case for the particular status code.  The QUIC version is sent, but because QUIC doesn't have any any guarantee of ordered delivery, it only kills the one half of the stream.  The QUIC variant needs a special case.)

Christian: Say viewer decides not to watch video. Is this an app or transport issue?

Mike B: Send FIN for request, then STOP sending.

Jana: Should we support more than the GQUIC use case/functionality?

*resume presentation*

Option: take STOP_SENDING to application layer, RST_STREAM is unidirectional
(but app signal has to be reliable (in a different stream))

EKR: this is an API issue

Jeff: no you need stream id credit from the peer

Roberto: there are two desirable behaviors apps may want. does this require two transport concepts?

Without negative flow control credit, no.

Bishop: Demanding the FIN is probably an app issue

Fernando: but apps don't have that channel!

Igor: suppose app encodes 2 giant streams and closes. rcvr wants to stop one, but the peer app is gone.

Mike B.: that's a good case to have a transport-layer semantic.

Bishop: rename to CANCEL_WRITE and CANCEL_READ. Maybe CANCEL_BOTH too? Word "reset" has too much TCP/HTTP baggage.

Duke; is this flush or fin?

Mike Bishop: dropping all queues on the floor (flush) ?

Jana; there are ways to support the non-flush version

EKR: are these the appropriate semantics?

Bishop: we need to handle directions separately; reliability is an open issue. but this might be an API issue?

EKR: as sender, we have RST and FIN. as rcvr: throw it all away.

Thomson: also as rcvr: please finish stream ASAP

Duke: does this address the actual objections?

Bishop: this makes everyone equally unhappy. Victory!

Ian: i agree with Mike that the status quo is good enough.

Duke: what is change from status quo?

Bishop: we want to keep in the same for now.

Jana: i would like to have CANCEL_BOTH

Ian: status quo -05 is cancel_both = stop_sending + rst_stream + return of rst_stream

Ian: -04 and before: rst_stream + rst_stream

Jana: actually i don't want cancel both

Bishop: rst_stream is an app decision to respond or not. better send stop_sending if you don't want the data.

Duke: the only quadrant we haven't covered is demanding a fin from the peer? is that OK?

Bishop: we think so, but will talk about it.

Bishop: api for streams would probably allow shutdown of read, write, or both, like file descriptors

Bishop: when is closed not "closed"?

in good case with two FINs and acks: what does closed mean? what state of delivery certainty is implied?

EKR: spec says when fin is sent

sender state machine: open, app finsihed, all data sent, all data acked + reset sent & acked

EKR: could also declare closed when exiting stream flow control

Christian: what if i receive a stream frame for a closed stream

Receiver states: open, knows final offset, received all data, delivered all data, reset received, delivered reset to app

Christian: point of closed is to get rid of stream state

Jeff: do proxies have to deliver all acked data before tearing down due to reset?

Christian: rcvr also has step where all acks have been acked

Jana: have to be careful about resets to keep flow control right.

Igor: for proxies: ack does not guarantee delivery to sender.

Jeff: what about proxies across protocols? http1 over tcp fin must map to the right stream semantic.

Duke: the issue is app may send rst_stream indicating that acked data is good but rest is unneeded. proxy may be elsewhere

Igor: same issue may arise if endpoint hasn't delivered to app

Jeff: must deliver the stream of bytes.

Buck: some protocols break large uploads into smaller chunks to avoid these issues. giant files should be discouraged.

Jeff: need to deal with legacy clients (e.g. http over tcp) -- semantics need to map

Victor: consider 1-direction stream - 3 states: open, finished, dead. are there other transitions?

Bishop: it fits in with my state machine

Thompson: what Jeff wants is a bad idea, but i can accommodate it. if we allow stream frames sent after reset, it works

Ian: that's fine if there is another reset type

Ian: we shouldn't have reset acked. that can be taken out of the stream state and in the transport.

Jana: consider http use case. if this is a real use case, we can support it. this state machine doesn't require anything of implementations but is useful in the abstract.

Christian: how does this interact with the FIN?

Bishop: we could have an alternate FIN where the max offset is below the actually max offset.

Victor: streams are kinda like messages. we shouldn't support this because peer can alter semantics of sender's stuff.


*break*

Roberto: Progressive video is bad for live. Even small segments -> latency. instead increase sizes of segments. mechanisms are over http. longer segments -> better latency and/or quality.

But we need to have adaptive bit rate with short reaction time.

at certain boundaries we need to stop, but deliver earlier stuff reliably

Igor: can app signal this need to transport?

Roberto: can mess up caching, etc.

Buck: why can't the chunks be separate resources?

Roberto: live stuff: don't want to have dynamic manifest

Buck: why can't you just ask for each chunk

Roberto: that's not http

Victor: can this be the http-over-quic mapping? problem that we don't know exact offsets.

Roberto: not access to OOO data!

Victor: we can't partially close because of variable length

mnot: we're ratholing. take offline.

Ted: this may not be generalizable.

Bishop: more expanded set of stream states useful as a concept in the doc?

room: yes

Bishop: close enough that I should write it up?

Victor: separate api and wire concepts

room: yes, write it up

result: We will discuss Roberto's issue offline

#### Unidirectional Streams

Others proposed, EKR tried to implement

took about 16 hrs to implement under bad conditions (not a lot of work)

exists in minq branch

recap: streams are initiated by sender; simple state machine; no odd/even semantics; can declare stream relationships (1:N)

Data structures are kinda similar

Streams hold a ptr to their related stream
this relationship is reported to the application but otherwise doesn't matter

His API doesn't work with many-to-one

Disadvantages: a little more work for bidirectional protocols

closure semantics unclear

mapping could get out of sync

"related streams" rules are awkward

Advantages: easier to implement, clearer semantics around creation, more flexible semantics

Jana: problem with max_stream_id but can't articulate

EKR: i haven't done max_stream_id yet, so maybe

DKG: I have to keep outgoing stream even though it's done, to understand the response

Victor: bidirectional state machine is product of unidirectional states. so what's the point?

Duke: When there is a receive stream you create a phantom stream for that. Why is it necessary?

EKR: Only necessary when doing bidirectional streams. Assuming if you use the bidi API you want to do that.

Praveen: can we have a collision of streams with simultaneous open?

EKR: no. stream id space is distinct.

Kazuho: is the only difference if they have distinct stream ids?

EKR: pretty much

DKG: main difference is flexible semantics. Is this valuable or not?

Peter: i agree with dkg: 1:1 and unpaired are cool; 1:N is horrifying

Ian: i agree with peter

Jana: what is common case? we should optimize for that.

Eric: not just if it's useful. can implement on top of anything. what is the common case?

Tommy: bidirectional API talking to uni API: must work. how to represent 1:N to a bidirectional API?

EKR: that's incoherent. stomp the receive stream and graft together, or reject it. application error?

Victor: 1:N not popular

Ted: explicitly signal over the wire if stream is uni or bidirectional. concrete non-bidirectional use case will help us figure out the details on how to do this, defer for now.

Let's not rewrite all the code now without a spur.

Bishop: 1:N is interesting for pub/sub. Request/response/push relationships in HTTP might allow all this stuff to move up to the application.

TCP apps -> bidirectional; UDP apps -> unidirectional

Jeff: common case is bidirectional. udp apps are unreliable and won't go to quic anyway.

Jana: effect on push streams?

Bishop: promises are in a different id space so that these can be limited.

Praveen: harder for implementations to step back

Roberto: 1:n stuff is totally orthogonal

EKR: a little early to ossify based on early implementations

eric: agree with eric, but should look at pros and cons. we have a 1:n use case. endpoint negotiates further comms on one stream, then transfer happens on extra stream. but i don't see how to do that in quic rather than the app.

Bishop: i disagrees with Jeff. websockets and other message-oriented protocols will be here.

Kazuho: in -05 the state machine is the same either way. keep current design. ian's proposal is most balanced.

Jim: Ted + 1. wait for pressing use case to change stuff.

Victor: unidirectional apps would benefit from this. e.g. mosh to QUIC

Ted: EKR is right, stuff will change. supporting the use case is great, but we shouldn't blow away the current framework.

Jana: ted+1. Kazuho+1, Praveen+1. existing implementations matter, will speed adoption.

Alan: can have imbalance between # of allowed request and response streams.

Jeff: we can do it all using current features, no need for more

Ian: my proposal that people are talking about: take a bit in stream frame that peer should immediately move to half-closed. making this explicit is nicer for proxies.

peter: Bishop+1. ted+1 (why not both?). i am building a message protocol with lots of streams. proposed in w3c as part of the web api. avoiding even/odd recovers half the stream space. (any link to the proposal available?).

Thomson: i am shocked at how this developed. just trying to solve a few bugs, which are not addressed in this discussion. real quic apps won't need bidirectionality. differences between EKR and ian are minor, just how we identify return half. ian+1

Thomson: stream 1 is currently broken in http if server speaks first

Christian: would like to resolve uncertainties in protocol. can we handle this with version numbers to test EKR's stuff?

Roni: unidirectional needed for multicast

Victor: we kind of want both. might be an implementation detail.ian's proposal might not work if we don't get the first frame first. makes proposal (see Thomson below)

Thomson: Victor+1. 3 types of stream frames: unidirectional streams, streams that expect a response, streams that are a response. Each has its own number space.

Roberto: I am happy with that.

EKR: must expose bidirectional API. Victor's proposal is fine. editors can work out details. must resolve issues of implicit stream creation. Victor solves this problem. i can do a new version as Christian says, but if people like Victor's idea let's go with that.

ACTION ITEM: Martin will generate a PR reflecting Victor's idea.


## 5 October 2017

Mark: we seem to be bouncing back and forth between API and protocol details.  He believes that a short document that describes the transport abstractions and guarantees.  He has asked a couple of folks to form a design team to produce that, as way of distilling the material for discussion.  Roberto and Jeff have taken the token for that.  May not be done for Singapore, but should be in time for Melbourne.  This will be a closed design team, but they may ask others for help (as a reminder, design teams have no special status in IETF process).

Lars looks back at yesterday and notes that we have 50 people in the room, but about half did not speak during the meeting.  Good break discussions, but we need more involvement from implementors--jump in when you need help removing a block.  Volunteer to write something up that describes the problem or a solution.  The effort on the implementations is great--we're up to 10 implementations.  But that isn't enough; you need to help write spec and write code.  Note that in an open process, we don't want to limit attendance.  But we do note that getting large venues is difficult and that having folks who are not talking in the sessions is worrisome for flow and impact.  We need to have more participation.  

Mark highligts as well that we are missing some diversity as well--there are zero women in this room.  If you have colleagues who can come to Singapore or Melbourne, please bring them along.

Jana: the editors are also happy to take information from implementors as issues and PRs in github; they can help guide the editors on what to work on next.

### Architectural Issues (cont'd)

#### ACK Frame

* [Issue](https://github.com/quicwg/base-drafts/issues/644)
* [Presentation](https://github.com/quicwg/wg-materials/blob/master/interim-17-10/ack-recovery.pdf)


Ian Swett presents.

The goal of the presentation is to first review things we agree on (4-5 slides) and then get feedback on formulation and open issues for anything that we do not agree on.  The last bit is an issue on timescript and ECN.  

Reviewing slide 1, QUIC Ack Principles.  

Jana notes on bullet one that this is different from TCP, and that the distinction needs to be kept in mind.  On bullet two, suggested replacement text is that Frames are not required to be retransmitted verbatim, but the information within them is retransmitted.  (Pure verbatim recapitulation will not work because of timestamp data).

Marteen asks about handshake retransmission and notes that he is concerned about the text about ACK frames.  He suggests either removing ACKs from the handshake retransmission and sending a new retransmission.

Ian: this is the intention.

Jeff: we may wish to highlight that retransmitting is generally the wrong formulation, except for the handshake.

Ian and MT are going through the document trying to remove the language around "retransmission" where the text needs to be rephrased.

On bullet 3, Marteen asks where the number 255 comes from--8bit number of ACK locks.

On bullet 4, Jim asks what "processed" means in "received, decrypted, and processed".  These are the transport rules, not the application processing.  So validate the frame, mark things off, and buffer the data.

Jim asks why you aren't done after authentication?

MT: if you have received something malformed, you would have to send a connection closed; that's part of the processing.

Christian: if you send an ACK for the MAX Data, you know it has been received.  That's what you want to achieve.

Jim: this is a bit slower than optimal, since you can't ACK until you've done processing.

Jana: you can't know whether you will be generating an ACK until you've parsed the transport-level information (since we don't ACK ACKS).  So processing is "transport-specific processing", not processing of stream data.

Jana: if you have sent an ACK and can't buffer the data, then you have no way to tell the peer that you need the peer to resend, so you should not send them until you have reached the point of buffering them.  You would have to reset the stream in that case, because you are otherwise not synchronized.

Jeff: there is a corner case when you have a half-closed connection; Ian notes that the processing is different in that case, but it is still transport-level processing complete.

Roni asks if you can send a connection close rather than an ACK.

Ian answers that connection close is always terminal, so you can send that without an ACK.

Bryan then noted that there are cases where you might have scheduling delay or busy processing.  We'll need more description of "processing" to avoid states where you violate the contract.

MT: the delay in allocating memory is okay, as long as you have not ack'ed to say that this has processing.  Essentially, if you fail to process and ACK, you are violating the contract and likely to get fatal errors.

Ian: you must protect ACK frames with protection equal or greater to the packets they acknowledge.

EKR asks about the possibility of promoting from cleartext to 1RTT key protection (or similar).  Should that be a should?  Definitely seems possible, but not clear how important promotion will be.

Jeff: the spec used to call this negative acknowledgement, but the language isn't clear on what to do.

Ian asks about whether an overview of the process would be useful.

Jeff agrees, and dkg suggests that he write it; Jeff agrees to do so.

Moving on two slide 2, ACK_FRAME: When to send them

Christian believes that bullet 3 is a fine goal, but given that some networks do have packet reordering, so it may be valuable to wait.

Ian, that's why this is "sooner", but not immediately.  (Note that this goal is not in the draft currently, so text is needed to describe).

Jeff: there are some things implied in the document (e.g. the 3 packets after a gap language)--there are a couple of pieces of suggested behavior that imply this, in other words, but not explicit text.

Ian: particular example is an interesting one, as the scheduling of ACK creation is still not easy to follow.

Praveen believes that we need to specify why we are deviating from TCP's behavior.  In some cases (high bandwidth cases), TCP is already deviating from the common case, so we can deviate when we have a reason.

Jana agrees that there are places where TCP is already deviating from once every two packets.  The gap behavior in TCP is already a SHOULD, so there are cases where it is already okay not to send immediately on seeing a gap.

Jeff: the transport draft has some of this text, but that the congestion draft is very incomplete.

Jeff suggests that we have MUST-level prohibitions should be in the transport draft, but that SHOULDs and implementation advice should be in the recovery draft.

Ian asks if this an okay split?

Jana and MT agree that this is a good split, and Jana notes that this how it is described in TCP.  Notes that it would be good for new people to have a link between the transport draft and the recovery draft.

Jim wonders whether asking one side or the other to send ACKs of ACKs (both sides doing it is obviously bad).

Christian: ACKing ACKs serves to prune acknowledgement blocks.

Ian: the document currently recommends sending retransmissable data (e.g. a PING frame) to elicit an acknowledgement; this will allow you to prune.

Jim asks to review the example.

Ian: this came from an experience with a very high loss datalink.

Clarification that the example implies you have not received 9, rather than describing behavior on receiving 9.

EKR suggests that the PING frame elicitation is a bit of hack, given how early we are.  Possibly we should have a more dedicated method.

Ian asks him to open an issue to create a flag or similar method, so that an ACK frame requests acknowledgement without including transmissible data.

EKR agrees.

Igor asks whether gap frame are not acknowledgeable.

MT and Jana notes that this can result to parrot frames.

Marteen: excluding ack frames are not including bytes in flow for the purposes of congestion control or flow control, and that this results in a strange situation: ack frame of 500 bytes is counted as zero bytes.  One with a ping frame attached is 501 bytes.

Ian agrees, but notes that this is needed to keep flow control or congestion control from preventing the sending of an ACK.

Jim: the MUST NOT also means that you can't pad ACK frames in that case, which might be needed to avoid traffic analysis.  ACKing ACKs at some rate also helps hide which are ACKs.

Christian: there are cases where a congested link should still get some ACKs.

Ian agrees, but notes that congestion control for ack frames is under active research in TCPM, and we should track that rather than invent something here.

Mike asks if we could weaken MUST to MUST NOT send an ACK to every ACK only packet.

DKG: this will result in corner cases where every millionth packet isn't ACKed.

Roni: it is easy enough to include PAD or PING to solicit ACKs where they are wanted.

Moved on to slide 4: When to stop sending old Acknowledgements

Notes two alternatives which may work better in other environments.

MT: the first alternative (Send each ACK block for an RTT) may not work in a sparse send situation.

Jeff: I have implemented the second (fixed number of blocks) and that it appears to work, but he hasn't tested in high loss environments.

Moved on to slide 5: Recovery principles.

MT believes we should recommend favoring retransmission of old data, but allow transmission of new data first when high priority new data is available.

MT believes that there is no text on that now; Jana notes that it is in the recovery draft.

Jeff asks whether this is related to the text on stream 0, Jana notes that stream 0 is not necessarily high priority.

Jeff asks if there is text that allows you to send the same data in multiple frames, so you could get something like a simple FEC.

Ian: this is legal, but there is no text on this either way.

Roni asks about the RESET STREAM, Ian notes that you don't try to resend data when a stream has been reset.

Issues: Timestamps and ECN (Issues #774, #804, #698).

Growing consensus that these should be negotiated extension to the ACK frame.  BASIC ACK (ack blocks); ACK + TS (Status quo); ACK + ECN are different frame types.

EKR, the default would be BASIC ACK, and once negotiated, we don't need bits to describe whats being done because it is consistent?

Ian, yes.

EKR: we don't have a method for doing the negotiation right now?

Ian there is some design freedom around this--that is client requested and must support by responder, or full negotiation.

Mike: each side might want different things.  Ian, we would need to negotiate in each direction.

Jim: you may not know the nature of the network at handshake.

Jeff: would it be the case you want different things during transition?

Roni: for ECN, we need to know whether we are going to require support for this in the transport--if we don't do this, we need some other mechanism.

Jana: some kernels may not pass this up to the UDP layer or above.

Martin Duke would like to get the temperature of the room of the room for timestamps--is this vestigial or are there people who want it.

Roberto on negotiation was initially thinking you may need a new connection, but given that may result in new ECMP placement, we may need to actually making that negotiation remain on the existing connection.

Mike B. notes that he is not "fired up", but there are multiple congestion controllers that are delay based, and timestamps are useful, even though the current floating point format is not great.

Lars: the proposal is to remove the current timestamp format, and to ask those who want timestamps to propose something.

Jeff: if anything you have is connected to connection, will you need to renegotiate if you move the connection to a different network.

Lars: not for timestamps, since it is internal to QUIC; ECN needs to be negotiated at the IP level negotiation as well, so it is trickier.

3 questions: do we agree to remove TS now?  do we have folks interested in developing new TS method?  do we have folks interested in ECN?

Jeff adds a 4th to talk about how this works with connection migration.

Leif and Eric can work on a proposal for ECN.

Eric: I use TCP timestamps heavily, so we would be interested in knowing what that would mean for QUIC.

Daniel Havey notes that folks from timestamps and ECN camps are not expected to be the same.

Martin Duke asks about the text on the slide about "status quo"-- basic ack has no timestamp, but ack delay is retained.

EKR: would we also repair the ack delay format?  Not at the moment, but possibly future.

Martin, Jana, Christian briefly discuss what ack delay means here--while they are different from TCP timestamps and ack delay seems to be RTT calculation.  The QUIC timestamps are different.

Lars calls consensus for basic acks for now, with other groups proposing new timestamp and ecn.  Nobody has the token to develop a negotiation format until a new proposal for a different format; these proposals may or may or not include a negotiation method.

Jeff do you have to propose a time format?

MT expresses a proposal to replace the wording around ack delay time format.

Jana: it has actually been on the plate for a long time, but he has been hoping for a format change, which would make it OBE.

Jana: I believe that the timestamp format will be valuable in high traffic conditions, so he is willing to work on it, even as he is willing to let them drop for now.

Lars: is there a proposal now for ACK frame extensibility?

MT not yet, and it requires going off and thinking about what the format should be.

Roni: there is text about congestion control that reference timestamps, and these need to be adjusted as well.

Christian: you can do delay-based congestion control using ack delay, but it does not have half-connection measures.  To get that you need synchronization.


### Header Compression

[Presentation](https://github.com/quicwg/wg-materials/blob/master/interim-17-10/header-compresion.pdf)

*Alien baby slide elicits laughs.*

Mike is concerned that we are in analysis paralysis.

Mike: each has learned from the other; there are a small number of ways in which the drafts are different.  If we can resolve those, we may be able to merge them and move them.  First major difference:  how you handle deletes (slide 3).

Jeff asks for confirmation that the decoder was very limited, the encoder had all the complexity.  qcram is closer to that.

Jeff: this is a nice property, if you don't have to validate at the http layer.  QCRAM could be changed to avoid that layer violation.

Buck: I believe that the contract between the transport and the mapping layer is a bit stronger than with the application.  The explicit acks could even be negotiation.

Alan: what pieces of qpack actually violate that contract?

Ian: there are other applications where having an ability to get a callback that says when something has been delivered.

Jeff: this is separate from the level of intelligence in the decoder

Ian agrees, these are orthogonal.

Jana: agrees that this callback would be incredibly useful.  He also notes that the explicit deletion requires work.  If there is complex code that gets exercises rarely, that makes him concerned.

Jeff: it actually gets used fairly frequent, as things move into and out of the table; eviction is frequent.

Dmitri: acknowledging a range of bytes means that there is a degenerate case in which you might have to track each byte as data may be reframed during retransmission.  This is too much to ask of a generic transport protocol just to support one use case (HTTP).

Jeff asks what the second disagreement is?  Stream reset is mitigated. (Jana notes that eviction may be less common for single server cases)

Buck asks if there is a lot of variability in table size--64k seems very common.

Jeff responds that there are a couple of common patterns.  For the case where you have a non-web client, you can have the special headers that are always in the table (they are never evicted).

Alan: this can be valuable in the web as well, so that some headers (e.g. user-agent) are never deleted.  Alan says that the core model difference:  do we have the encoder control this, or is this a circular eviction scheme.

Jeff, there are hop-by-hop changes (that is, a proxy may have its own sense of required headers etc.).  Mike notes that there is a mitigation for the roll-off case by adding a new one to the front.  The old one rolls off, but the new one is there to replace it.

Back to stream reset.  There is a possibility of the data loss in request streams in QUIC.  To avoid that data loss causing a loss of shared compression state, you might have a way to handle a "blessed stream" that handles data manipulation or you may correct that using recovering the control stream.

Jeff: push may mean that stream reset is not that rare (and there was then discussion of when and how resets occur, but the upshot remained:  streams may get reset).

Roy asks what the current table size is.  4k was common, then went to 16k and 64k very promptly.

Alan: the overhead per entry is different in the two approaches, and that means that the number of entries per a 64k table is different.

Alan wonders whether delete could be made optional, so that some folks could build naive implementations if you wanted.  If you ignore deletes qpack no longer has to worry about loss on control streams; that's not the same in qcram.

Jeff: don't follow.  If there is no delete, and the table is thus append-only, why isn't that same?

Jeff: this is pretty complex.  It may be concentrated in the encoder, but it won't be simple.

Roberto believes that tying this to a single stream may be fine, but that having an arbitrary set of streams could also work. That would be useful if you want multiple compression contexts.

Mike: if you want to do that you need to have a way to reference that context, but that this is otherwise possible.

Jeff: if you have different contexts, you can have resets restart with a new context.

Buck asks if things like push streams might be in different contexts.

Jeff agrees.

Roberto believes that the one stream or multiple streams is a bike shed.

Mike believes that this may be a bike shed, but the "unkillable" nature is likely not.

Roberto: this is not quite true, it simply means that the streams which refer to it must die.

Roberto also notes that HPACK chose a circular approach because it was simpler than delta encoding.

Mike is that ring buffer property considered useful enough to make deletion of specific items more complex.

Buck: the question of having one stream or multiple streams for the updates has some subtle effects--if one, you can get HOL, but if many, you can get real complexity of interleaving them.

Buck feels like the move to a single stream for updates was a useful simplification.  Alan notes that the headers block and the frame for the insert will go out together.

Roberto still believes that this is bikeshedding. So long as the sender is saying he is sending bytes in order, if the receiver sees a byte at an offset, they can choose to ack if they didn't care about those bytes.

Buck: the QUIC implementation at Google put all headers in a single stream and it was painful; we have skipped that presentation, but the pain is real.

Alan: this is a different issue, since it is only table updates, not all headers.

Buck agrees that this is different.

Alan and Jeff then discussed whether the proxies need to have the same set of updates to their tables and conclude that it is "it's complicated".

Mike: we have convergence that we want the encoder to decide when to a delete.  Note hearing a lot of convergence on the second point.

Jeff, do we have a direction, even if not convergence?

Alan and Mike disagree with Buck, with not a lot of other strong positions.

Roberto may have a clever tweak to improve the HOL, though not mitigate the issue entirely.

Discussion of value of retaining HPACK wire encoding elements into the follow-on wire encoding.  QCRAM augments the existing mechanism, but QPACK is a redefinition.

Buck explains that his choice was because there will continue to be fallback to h2 over tls.

Jeff: the pretty unicorn here is that shifting to QCRAM style augmentation with QPACK's stream approach; that would let you use a single encoder across both h2 and quic.

Mike: HPACK has some optimizations to avoid commands that cannot be used in some contexts.

Alan: they may be where they end up, but for his implementation he simply started over.

Mike: can we overcome our distaste and pick one already?

MT: we didn't get decisions did we?

Mike: we did get some, we agreed that the encoder should be fully in control of deletes.

Sense of the room on wire compatible for HPACK: stronger hum for willing to diverge.  Strongest hum for falling over from hunger.

*Lunch*

Mark: Not feeling much urgency here, but are people coalescing?  Sounds like a Buck-and-Mike design team.

Martin: Let's set a deadline and pick something people can start implementing.  We're getting interop in a bunch of things; we need to start using HTTP/QUIC.  Even something short-term, like leave out deletes and add them later, would let us make progress.  That's more important.

Jana: There's already a temporary solution -- use the static table only.

Martin: That can work.  So this is less urgent.

Mark: Then we'll announce a design team.

#### Data on HOLB

[Presentation](https://github.com/quicwg/wg-materials/blob/master/ietf99/FHOL%20results%20(IETF%2099).pdf)

Tweaked Google QUIC to tunnel all stream data on single stream to force HOLB on QUIC to measure it.  Measured network latence, user experience quality.  Not header compression, entire thing.

Latency of individual transactions:  Negligible at median, 1-3% worse at 95th percentile.

Difference between Windows & Android, believed due to hanging GETs artificially skewing

Experience latency:  0.16% slower search results at the mean.  Looks small, but is a noticeable move at Google scale.  Large moves on YouTube.

Roberto: Remember that there's survivorship bias.  The tail may dominate, but this is the tail of people who kept watching anyway.  The people who gave up didn't get measured.  Studies have shown that predictable experience is more important than raw performance.

Jeff: Reducing variance is important.

Buck: HOLB negligible at mean, 1-3% at the tail.  Maximum HOLB on the headers frame is 157ms delay at median, 2.6 seconds at 95th Percentile.

Jim: When the channel is saturated, you have to have prioritization to improve this.

Buck: In-network buffer bloat is a bigger problem; falling off the end of a queue hurts a lot.

Patrick: Are search and YT representative?

Buck/Ian:  Google not as conducive to connection pooling as it could be; web at large has more requests per connection.

Jana: The total wins of QUIC versus TCP are substantial enough, it can be expected to transfer reasonably well to the rest of the web.

Patrick: Google represents a really well-connected CDN; the rest of the web is likely worse.

Buck: Yes, this is conservative.



### Issue 693, AEAD Protection of Cleartext Packets

Concern about off-path injection of packets; EKR proposed using AEAD encryption with a Connection ID-derived key.  People didn't want to bake a single algorithm into QUIC for all time, but VN and SR are version-independent.

EKR: Didn't we already agree on this?

Christian: You're exposed to injection attacks until you have some shared key.

Jana: This gets rid of off-path attackers.

(Brief confusion between Stateless Retry and Stateless Reset.  Something needs a name change.)

Jeff: Section that describes Cleartext points to TLS; will replace description of hash.

Jeff, EKR:  Use different keys for client and server, have fewer Cleartext

Martin: Feed a client/server tag into the key generation, along with the version.

EKR to submit PR.

*break*


### Next Steps

Mark: Start to define a third implementation target as the basis of Singapore.

Christian: That's either aggressive or limiting.

Mark: Have we finished with the second target?

EKR: Clearly not.

*Discussion of the differences between -05 and -06, mostly not affecting the current targets.*

Mark: Would it be useful to discuss what we need to want to test next?

EKR: Only a few implementations are caught up already, let's not get further behind.  Keep the same scope and either stay on -05, or same features on a quickly-shipped -07.

Several, including Patrick:  -07.

Martin: Largest -07 changes are landing in the next week (some now); people can track the Editor's Draft until we publish.

Jeff: Will that include the ACK changes?

Ian: The removal of timestamps yes; ACK guidance probably not.

Mark: Please summarize what will be changing in -07 -- assign issues to a milestone.

Martin D.:  What do people currently not have?

EKR: Stateless retry.

Jeff: Should add 0-RTT.

Christian: What happens if someone proposes an old version?

EKR/Martins:  Whatever you pick.  Are you a dual-version implementation, or will you do VN and fail if you don't have a mutual version?

Patrick: I'll probably leave my -05 endpoint available if people want to keep testing.

Jeff: Let's also try changing the connection ID.

Patrick: Let's pick an ALPN token for http/0.9 and keep it fixed.

Mark: Not "http/0.9" -- want something ugly no one will actually try in the wild.

Jeff: URL of the HTTP/0.9 spec?  "418"?

Other suggestions:  hq-05, bikeshed

Mark: Poll on Slack.  Move on.  We're using the same Wiki page for the second milestone; who's going to update the page to have more granularity?

Jeff: Test cases would be useful.  Would love to contribute a test client, but that's more complicated.

Mark: A hero will emerge.  Assume there's a wiki -- everyone dump your test cases there for others to leverage.

Will revisit a refined second implementation milestone, but using draft -07.  We'll be more aggressive for Melbourne.

EKR: In TLS, there's a "max early data" value in the session ticket, and most implementations won't do 0-RTT if it's not indicated.

Martin: Use QUIC's MAX_STREAM_DATA to control this for real, but need to mandate that it's included in the ticket to make general-purpose implementations happy.

Mark: In Singapore, two sessions; one devoted to middleboxes.  Report from interop, more architectural issues to discuss.  Reports from design teams (middleboxes, abstractions, and header compression), though may not be done by then.

Martin D.:  Are there ECN or Timestamp design teams?

Mark: Not yet, but please inform them about our discussion and steer them into starting one.

Adjourned: thanks to F5 for hosting!


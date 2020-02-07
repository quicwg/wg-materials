# QUIC February 2020 Interim Meeting Minutes

* Chairs: Mark Nottingham, Lars Eggert, Lucas Pardue
* Location: Zurich, CH
* Scribes:
  * Wednesday morning: Brian Trammell + Sean Turner
  * Wednesday afternoon: Eric Kinnear
  * Thursday morning: Sean Turner + Brian Trammell

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
- [Wednesday 5 February](#wednesday-5-february)
  - [Interop Summary](#interop-summary)
  - [QUICDISPATCH](#quicdispatch)
  - [Transport, TLS, Recovery, HTTP/3 and QPACK Issues](#transport-tls-recovery-http3-and-qpack-issues)
    - [\#3294 Make transport parameter ID and length varint](#%5C3294-make-transport-parameter-id-and-length-varint)
    - [\#3126 Timeout Connection Close error](#%5C3126-timeout-connection-close-error)
    - [\#3215 Timer interval for retire the connection IDs](#%5C3215-timer-interval-for-retire-the-connection-ids)
    - [\#3333 Padding outside QUIC packet](#%5C3333-padding-outside-quic-packet)
    - [\#3373 More Strongly recommend ECN marking](#%5C3373-more-strongly-recommend-ecn-marking)
    - [\#3332 Composability of QUIC Extensions](#%5C3332-composability-of-quic-extensions)
    - [\#3216 Flow Control Tuning](#%5C3216-flow-control-tuning)
    - [\#3348 Which DCID do Handshake retransmissions use?](#%5C3348-which-dcid-do-handshake-retransmissions-use)
    - [\#3304 ACK Generation Recommendations](#%5C3304-ack-generation-recommendations)
    - [\#3350 Ignoring ACK delay can lead to wrong RTT](#%5C3350-ignoring-ack-delay-can-lead-to-wrong-rtt)
    - [\#2923 MIN_RTT management](#%5C2923-min_rtt-management)
    - [\#3215 Timer interval for retire the connection IDs (post lunch)](#%5C3215-timer-interval-for-retire-the-connection-ids-post-lunch)
    - [\#3348 Which DCID do Handshake retransmissions use? (post lunch)](#%5C3348-which-dcid-do-handshake-retransmissions-use-post-lunch)
    - [\#3161 Simplify the client\'s PTO code by allowing the server to send a PING](#%5C3161-simplify-the-client%5Cs-pto-code-by-allowing-the-server-to-send-a-ping)
    - [\#3335 Immediate retransmission upon loss detection](#%5C3335-immediate-retransmission-upon-loss-detection)
    - [\#3078 Lost Server Initial Takes Too Long to be Retransmitted](#%5C3078-lost-server-initial-takes-too-long-to-be-retransmitted)
    - [\#3094 congestion window increase on every ACKed packet could result in bursty sends](#%5C3094-congestion-window-increase-on-every-acked-packet-could-result-in-bursty-sends)
    - [\#3259 Safety issue during incipient persistent congestion episode](#%5C3259-safety-issue-during-incipient-persistent-congestion-episode)
    - [\#3272 pto\_count should be reset when dropping a packet number space](#%5C3272-pto%5C_count-should-be-reset-when-dropping-a-packet-number-space)
    - [\#253 HTTP/QUIC without Alt-Svc](#%5C253-httpquic-without-alt-svc)
    - [\#2223 When can you coalesce connections](#%5C2223-when-can-you-coalesce-connections)
    - [\#3423 active\_connection\_id\_limit is unknown for 0-RTT](#%5C3423-active%5C_connection%5C_id%5C_limit-is-unknown-for-0-rtt)
    - [\#3413 Does the amplification limit apply to PTO packets?](#%5C3413-does-the-amplification-limit-apply-to-pto-packets)
    - [\#3420 Forced connection ID retirement](#%5C3420-forced-connection-id-retirement)
    - [\#3408 Is absence of both :authority and Host an error?](#%5C3408-is-absence-of-both-authority-and-host-an-error)
    - [\#3418 Order transport parameters](#%5C3418-order-transport-parameters)
- [Thursday 6 February](#thursday-6-february)
  - [Zombie Issues](#zombie-issues)
    - [\#3353 Description of Preferred address CID](#%5C3353-description-of-preferred-address-cid)
    - [\#3428 H3 guidance on CONNECTION\_CLOSE does make clear if the type is 0x1c or 0x1d](#%5C3428-h3-guidance-on-connection%5C_close-does-make-clear-if-the-type-is-0x1c-or-0x1d)
    - [\#3427 active\_connection\_id\_limit description is unclear about whose connection ID might be zero length](#%5C3427-active%5C_connection%5C_id%5C_limit-description-is-unclear-about-whose-connection-id-might-be-zero-length)
    - [\#3423 active\_connection\_id\_limit is unknown for 0-RTT](#%5C3423-active%5C_connection%5C_id%5C_limit-is-unknown-for-0-rtt-1)
  - [Extension Drafts](#extension-drafts)
    - [Version Negotiation](#version-negotiation)
    - [QUIC-LB Update](#quic-lb-update)
    - [Datagram](#datagram)
    - [Ack Frequency Extension](#ack-frequency-extension)
    - [Multipath Extensions for QUIC](#multipath-extensions-for-quic)
    - [QUIC Loss Bits](#quic-loss-bits)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->



## Wednesday 5 February

### Interop Summary

See the [interop
sheet](https://docs.google.com/spreadsheets/d/1D0tW89vOoaScs3IY9RGC0UesWGAwE6xyLk0l4JtvTVg/edit#gid=535093126).
Still playing catch-up with changes in the draft.

### QUICDISPATCH

Extensions to QUIC to be discussed in a special experimental WG session
in YVR, which may become its own working group. Discussion about whether
all applications belong in QUICDISPATCH, or only applications that might
be extensions, or only extensions. Experiment to deal with built up
pressure around modification and extension proposals, need an overview
of work in the space.

### Transport, TLS, Recovery, HTTP/3 and QPACK Issues

See the \[[project
board](https://github.com/quicwg/base-drafts/projects/5)\].

#### [\#3294 Make transport parameter ID and length varint](https://github.com/quicwg/base-drafts/issues/3294)

David Schinazi: current transport parameter encoding dates back to TLS
presentation language. 16bit ints everywhere. Length prefix serves no
benefit. Everything else is varint. Increasing IANA registry space from
16 to 62 bit also a benefit.

ekr: why is length unnecessary?

David: Vector length is repeated, -2. Length of each transport parameter
is still necessary. Idea is to reduce redundancy. Change is small and
self-contained. More difficult to change in future. You can't fix this
as an extension since it's the extension mechanism. Maybe changeable in
v2.

Martin Thomson: Maybe not, if you change it in v2, you have transport
params with the same codepoints, which is interesting in a bad way.

ekr: Arguments against this change: 1. let's not change things. 2. If
you do this work in the TLS part of the stack \[unintelligible\].
Removing length itself is OK for TLS stacks, varints are less easy.

Martin Duke: Is version negotiation dependent on transport params?

David: Current design has a concept of compatible versions, this could
be incompatible in the future.

ekr: If we don't make this change, and we run out of codepoints...

Ted: If we get to exhaustion, before we get there the bar for
registration goes up. If we think we'll hit the narrowing function, we
should take the hit now.

ekr: Exhaustion isn't the argument here, collision is. Collisions almost
always come from picking the next spot in the space.

Jana: Was opposed because I think it's cosmetic. Exhaustion is not a
problem. Collisions are real, not a significant problem.

Ian: Could save bytes in the Client Hello, since everything we send
today would fit in one-bit

Marten Seeman: Privacy improvement if we give control of parameters to
QUIC, since we could reduce the fingerprinting surface by forcing
ordering.

ekr: Could also force ordering in TLS. Was opposed, but if we ever want
to do this we should do it now.

Kazuho: This change would keep implementations from reusing the TLS
encoder for transport params, opposed but if others think

Martin D: I'm with ekr on this. Risk of v1/v2 incompat would be sad.

Brian T: Feels like a future CVE, let's make the change.

Matt (and other implementers): this would be annoying but it's not the
first time, open to the change because it is cosmetic.

spt: anyone willing to fall on this sword?

Jana: how sharp is it?

Jana: We should not lose the principle that we don't want cosmetic
changes. But if implementers are willing to do it. No precedent for
cosmetic changes.

Proposed resolution is to merge the [PR
\#3169](https://github.com/quicwg/base-drafts/pull/3169).
Assigned to Martin Thomson for consensus call and merge.

Ian: If we make this change, please ship -26 earlier to give
implementers time \[general assent\].

#### [\#3126 Timeout Connection Close error](https://github.com/quicwg/base-drafts/issues/3126)

Mike Bishop: We already have this error code \-- it's NO\_ERROR.

Rui: Rationale is, the client may want to know why the server closed the
connection.

Jana: Doesn't that expose the server's state machine?

Rui: You could have an error description with no error, but that seems
weird.

Jana: Agree with Mike, this seems like no error.

Mike Bishop: Do we need text telling you to use no error?

Ian: We have it.

Mike Bishop: Okay, close with no action.

Proposal: close with no action.

#### [\#3215 Timer interval for retire the connection IDs](https://github.com/quicwg/base-drafts/issues/3215)

Martin T: Need to be prepared to receive packets with a given connection
ID that has been retired. After that period I might send stateless
resets instead. Recommendation 1, promptly retire. Recommendation 2:
have a timeout. This made me reconsider the whole design.

Jana: You need this period for reordering etc.

Martin T: PTO is used to drive loss recovery. In this case we're getting
stateless resets.

ekr: Value needs to be ultraconservative.

Brian: Why would you do retire and reuse? Seems to me the most
conservative thing is retired connection IDs are retired for the life on
the connection.

Ted: Why don't you want consistency in behavior here? There is some
implicit assumption that your connection is linked to the path.

Igor: Sender who already acked retired frame will forget stateless reset
token

Mike B: Client has not retired those connection IDs.

Igor: Assume acked the retire frame.

Mike B: It acked the retire-prior-to.

Martin T: Ted's point is the central one: design implicitly assumes CID
is bound to infrastructure on a path. One of the reasons we did
connection IDs was to have a routing ID independent of that stuff.

Roberto: There is no good answer to this. Tradeoffs are not obvious: do
I want a new CID for path awareness, for path obliviousness? The timeout
in each case, who knows? Do something. Not going to be perfect.

Ted: Everything isn't quite as ruined as MT asserts. We're not storing
something that is fully path fixed. We're saying if you're actively
moving to the path, you can signal to the path (e.g. load balancers)
that this is where you're going. We haven't lost nat-rebind by doing
this. If someone ages out connection IDs, it might give you the old ones
back. If the path infrastructure hasn't changed, you can reuse it...

Eric K: Contention here is how long should you wait before breaking
connection for still using the CID. Giving people more time is not
necessarily bad.

Lars: Earmark and take it to lunch?

ekr: Remember it for purposes of not sending a stateless reset. You can
not reuse it while not remembering it by keeping an encrypted counter.
We have in general refrained from using ACK as a state machine
transition.

Roberto: So long as we fail quickly it doesn't matter if it's a
melt-your-connection since we can create a new one.

Mike B: This happens where the client has failed to do something it's
supposed to do. The alternative is to close the connection immediately.
This is strictly less bad than not having the mechanism.

Jana: Text in the draft. non-normative, if peer doesn't retire rapidly
enough it risks stateless resets. Question is how much tolerance the
server should have. Currently 1PTO. Could make it 3PTO.

Decision: Jana will lead a lunch group.

#### [\#3333 Padding outside QUIC packet](https://github.com/quicwg/base-drafts/issues/3333)

Martin T: Basic question: Does garbage in the packet count toward your
amplification limit? Three proposals:

1.  If you can process a packet in a datagram, then the entire datagram
    counts.

2.  If the long-header is something you understand, then the entire
    datagram counts.

3.  If you process the datagram, then the entire datagram counts.

Kazuho suggests MUST/SHOULD/MAY, I suggest MUST/MAY/MAY, Marten Seeman
suggests MUST/MUST NOT/MUST NOT.

Roberto: How do you enforce the MUST NOT.

Marten S: We are doing interop with primitive setups, where datagrams
will probably arrive. In more complicated networks, datagrams will
probably not arrive.

David S: Let's say the client is sending something to the server, e.g.
no 0rtt keys available, in this case we can't distinguish valid from
garbage. So we have to count them,

Dmitri: How would you count these?

Martin T: If you've received something on a 4-tuple, you can count it.

Dmitri: But you don't have to.

ekr: If I receive an initial, then I send a retry. Am I then allowed to
send 7200-retry octets?

Marten: Nope.

Kazuho: In case where client sends 1201-octet hello, then server acks
1200, then client sends 1 octet, and that gets lost and retried. Server
window goes down by one byte per.

Ian: Was strongly in favor of must/{may,should}/may. On the last point
about complete garbage, what happens with multiple connections on the
same 5-tuple. I'd be fine with MUST NOT on the last case.

Martin T: Can I distinguish that from case 2?

Ian: I mainly just care about the 0RTT case, because it's common and has
to work well.

ekr: attacker generates 1 junk packet and two valid initials, now you
have an arbitrary amplification problem. Three principles in tension:

1.  Don't amplify

2.  Ease of implementation

3.  ? what Marten S wants.

Marten S: Kazuho convinced me that accepting 0rtt without keys makes
sense. So I propose must/must/must not now.

ekr: I receive an initial, and I'm slow, so I get a second initial
\[missing\]

Mike: First is definitely MUST, ekr's argument is that third is MUST
NOT. Can we split the diff and SHOULD case 2?

Martin D: Dangerous, could lead to deadlock, because a server might make
a choice to count retries where the client doesn't.

Martin T: Can we reformulate 2 to "can be uniquely attributed to a
connection"?

Martin D: I think the proposal is now:

1. If you receive a valid packet, MUST account for entire datagram

2. Otherwise, if you receive an apparently-valid packet you can't
    decrypt, MUST account for the entire datagram

3. Otherwise, if you receive the packet, ??? account for the entire
    datagram.

David: do we need to say anything about case 3?

ekr: if we take Martin T's suggestion, then no.

\[ekr and christian discuss quickly with an aggressive low-pass filter
and a lo-fi guitar reverb applied\]

Lars: sounded like we had consensus, except Christian. Trying to
converge.

Jana: Need to attribute to a connection to find the keys to decrypt it.

ekr: Whole point of this is that you can't cryptographically attributed.

Lars: Rough consensus for "For the purposes of avoiding amplification
prior to address validation, servers MUST count the bytes received in
datagrams that are uniquely attributed to a connection. This includes
datagrams that contain packets that are successfully processed and
datagrams that contain discarded packets".

Jana: What about entirely junk datagrams?

ekr: As long as they are uniquely attributable.

#### [\#3373 More Strongly recommend ECN marking](https://github.com/quicwg/base-drafts/issues/3373)

ekr: Should we urge people to use ECN? Should we assume ECN will work
and back off if not (default on), or should we assume that will not
work.

Mirja: The algorithm there is more complicated than it needs to be,
based on measurements.

Jana: We try ECN if it works great use it.

Lars: QUIC is a chance to make ECN happen more quickly. Will be more
useful for media than H3. We will want this. Doesn't need to react to
ECN marking, but the network needs to see a lot more ECN on UDP.

Eric: We already pretty strongly recommend it. As a data point for the
algorithm, we have turned on ECN for TCP on Apple and fall back, it
works and it has for three years. Much simpler just need to turn it on.

Lars: Do you have ECN with UDP?

Eric: Will look.

ekr: Comfortable with text encouraging. Don't want to add more. Use
before validate is fine considering Apple's experience.

Lars: Arguing for "assume ECN works and fall back".

Ian: Moving to a more aggressive stance without data seems dangerous.

Matt: to be clear, do we want to more strongly encourage? Current text
is not that cautious. Recommending "SHOULD ECN" seems a little strange
without more experience.

Jana: Specific issue is about sending 10 ECT0 packets, and if all are
lost, then disable. Other packets can be sent with ECT0. Mirja suggests
mark everything.

David: I like ECN. Apple turned it on. It went well. This is not
required for interop, it's a local implementation matter. In practice,
nobody is going to do what the spec says. Apple has centralized path
sensing. Chrome will do its own thing.

Brian: We should get the internet used to ECN, Apple was a good start,
and future QUIC features will appreciate its use

\[unintelligibly quiet\]

Roberto: Premature to recommend a specific algorithm. 10 packets might
suffer a correlated loss, so an algorithm that senses ECN drops with 10
packets might have false positives.

Matt: We'll experiment with this over the next year.

Mirja: One option is to remove the 10 packets paragraph. Minimum change
is editorial to note that this is low connectivity risk based on data.

Martin D: Doing stuff in the draft might not drive deployment. People
who want to see this happen should talk to implementers and persuade
them.

Eric: Issue is that alg is too specific, so we should remove it. We can
also leave it as is.

Jana: We do recommend ECN in the draft. In terms of alg, the draft has
one now. Lowest cost path is to leave it as is. If people think the alg
should be simpler or different, that's the Q.

Roberto: Move on (please)

Lars: either we leave as is, or we back off and say do it but not
specify what that is.

Jana: We can do something but it doesn't need to be perfect.

Mirja: We could just remove it because this is not QUIC-specific.

Ted: Keeping strategy in here until we have something better, we need to
say something.

Mirja: Close with no action, I'll send an editorial PR to make this
sound less scary.

#### [\#3332 Composability of QUIC Extensions](https://github.com/quicwg/base-drafts/issues/3332)

ekr: we can't stop future us from being dumb, but this is the easiest
way to detect it.

Christian: \[unintelligible\]

Martin T: No feedback on your draft, because it's not core, we're
focusing on that.

Lars: High level issue: if there are conflicts between extensions, how
to work that out ahead of time? Difficult. Natural order, first through
the publication gate wins.

Igor: this doesn't need to be done in the core draft.

Lars: Any argument for something other than close with no action?

Mike B: Extension section of HTTP says There Be Dragons Here.

Lars: we can add text that says please look at what is previously
defined (i.e., there might be dragons here).

#### [\#3216 Flow Control Tuning](https://github.com/quicwg/base-drafts/issues/3216)

Martin T: We say nothing about flow control tuning because loss recovery
is decoupled.

Jana/Ian: not sure this is design.

Matt: This has come up during interop testing, but in general it's not a
problem. Clients are strange. Do not think we need a change.

Jana: We have enough in the draft now.

Roberto: Two parts are potentially interesting: how much window are you
willing to have, how and when to update. We can minimize inefficiency if
we require an update to be sent when there is a change. Possibility
exists to limit damage. Important to get right regardless of whether
there is text in a draft.

Lars: Proposal - close with no action.

#### [\#3348 Which DCID do Handshake retransmissions use?](https://github.com/quicwg/base-drafts/issues/3348)

Ian: If you send a new connection ID frame in half-RTT packets, client
has a connection ID that it created initially, or a CID on Server
INitial or Retry, and now it has a \*second\* CID it could use for
retransmissions. What to do? Attitude 1: only change CID on initial and
retry, no CID change until 1-rtt, Attitude 2: you got a new CID so you
have to work with it. Implementation complexity is not that different?

Martin T: Coupling state machine with handshake state machine
complicates things.

Marten S: I make sure I never have to split crypto frames. 4-byte packet
numbers, can make sure a handshake retrans fits.

ekr: I hear people not in favor of changing.

Ian: Problem is ambiguity.

Lars: We should fix the ambiguity.

ekr: client ought to use the connection ID for the whole handshake and
not retire it, new connection IDs that happen during 0.5rtt can only be
used.

Brian: what ekr said basically. question is forbid new CID during
half-RTT, or accept it but don't use the CID until 1rtt. Don't see a
compelling reason to migrate before handshake is complete.

Ian: Forbidding is harder than waiting.

Eric: Design principle is don't mess with CIDs in handshake, we should
follow that principle.

Martin T: This would couple the state machines, which is uncomfortable.

Kazuho: Server can't retire CID used during Handshake anyway. It's
stupid.

Martin T: Not prohibited, but stupid.

Martin T: Throw this on the lunch pile?

Ted: Is this a "doctor it hurts when I do this problem"? Argument for
don't do this if it hurts you makes more sense.

David: Seconding Ted. Can we have an editorial change that says "BTW, if
you send a CID in half-RTT to the client it might use it."

Ian: I don't think we can fix this editorial; we need to clarify the
text one way or the other. My reading is that the client can't change
anything before handshake complete. No strong opinion.

Jana: We just need a decision.

Eric: Three options. Leave it ambiguous, let's not do that. Other two:

-   Can't set please retire to anything greater than zero unless
    handshake is complete.

    -   \...and allow new CID to be used by client before handshake is
        complete

    -   \...and prohibit new CID to be used by client before handshake
        is complete

-   No changing CIDs at all during the handshake; this is a bigger
    change. This is Ian's reading.

#### [\#3304 ACK Generation Recommendations](https://github.com/quicwg/base-drafts/issues/3304)

Ian: If you're interested, read the extension draft. On some
networks/devices QUIC can be more costly, TCP default of ACK every two
packets is costly. Turns out TCP doesn't actually do this, but TCP RFC
says this, so we do too. Ways forward:

1.  Make it a should and assume people will ignore it

2.  Recommend heuristics

3.  Defer to ack frequency extension

4.  Pull ack frequency design into core transport

Eric: Reducing frequency showed double-digit throughput improvement in
some cases. Current text puts a requirement on how many ack packets.
Some TCP implementations rely on number of ACK packets and not bytes
acked, which constrains TCP. Assumptions about how many packets may lead
to this in QUIC too, let's avoid that. I don't think we need explicit
negotiation if we don't make the assumption in the first place.

Roberto: This is flow control.

Kazuho: We need experimentation between different endpoints before
adopting a proposal. Defer to extension.

Mirja: Not saying anything seems wrong.

Jana: We do have a default that's more costly. That's a performance
point, not an interop point.

Lars: Consensus for close with no action, editorial to say that the
recommended rate is safe but not performant?

Roberto: Do we want to grease? Otherwise we get assumptions

Eric: Which is a problem with TCP.

Ian: Do we need to add ack frequency to the charter?

Mirja: Charter explicitly lists a set of extensions and ack freq is not
there.

#### [\#3350 Ignoring ACK delay can lead to wrong RTT](https://github.com/quicwg/base-drafts/issues/3350)

Ian: If you receive an RTT less than minrtt, you don't subtract ack
delay. This is a safety mechanism to ensure you don't get a too-low
smoothed minrtt. But if you're like 1us under minrtt, this has an edge
case, especially if you have lots of delayed acks. Current text is
safer. Suggestion is to cap: don't go below minrtt but allow the sample
to be at minrtt (rather than -ackdelay). Current text is smoother. In
practice, it does not matter that much.

Brian: In common case it reduces to the same behavior, right?

Ian: correct.

Martin T: this is intellectually appealing, but introduces different
skew.

Ian: I think the corner cases this proposal introduces are worse.

Jana: Propose no change.

Lars: Arguments against? Can also close the other minrtt one (2923)

#### [\#2923 MIN_RTT management](https://github.com/quicwg/base-drafts/issues/2923)

Jana: MIN_RTT scope is the entire connection, lasts for connection
lifetime. Currently used only for sample rejection for recovery
purposes. Gorry says MIN_RTT might increase over time, which skews
timeouts. For purposes of recovery, this is adequate. May not be
adequate for other uses of MIN_RTT, but we don't specify those.

Lars: Can we rename it?

Jana: Happy to look at an editorial PR to explain what MIN_RTT is used
for (and explain why stale MIN_RTT doesn't matter).

#### [\#3215 Timer interval for retire the connection IDs (post lunch)](https://github.com/quicwg/base-drafts/issues/3215)

Eric K: Lunch discussion resulted in the following action: Close with no
action. Open new PR to clean up text, but the actual recommendations are
good enough. Forced connection ID now in \#3240 .

#### [\#3348 Which DCID do Handshake retransmissions use?](https://github.com/quicwg/base-drafts/issues/3348) (post lunch)

Eric K: Proposal is to clarify that issuing CID means begin prepared to
seeing it used at any time. Additional editorial issue for packetization
issues.

#### [\#3161 Simplify the client\'s PTO code by allowing the server to send a PING](https://github.com/quicwg/base-drafts/issues/3161)

Ian: Do we allow server to also send Ping as it might help move things
forward?

Kazuho: Concern if an attacker injects a packet that looks like a very
small RTT between a client and server in which the real RTT is much
higher. Now the server retransmits many PTOs in a short period of time,
which results in a much higher amplification factor.

Ian: The exponential backoff means that in practice that you won't get
more than an extra datagram out of someone.

Kazuho: Even with 1mss? Ian: Yes, you end up with 10 packets.

Mike: The issue here is just number of datagrams, not the quantity of
data here. I'm not sure we care.

Kazuho: In PTO the server can send a full-size

Ian: Not in this case, this is a case where there's a restriction and
the server can only send a ping. If the server is limited by
amplification factor today it has to just disable PTO. Now, we'd want it
to send a ping, but nothing bigger.

Kazuho: I don't like making another special case, though. I don't think
that's going to make it simpler, it's just moving the goal.

Mike: You already have a special case, this just changes what you do in
that special case.

Ian: It does simplify the client's behavior, and I think it's less code.
Not saying we must do this, but it's not significantly more complex.

Christian: Do we allow the client to ping the server?

Mike: The client is not amplification limited, so yes.

Martin Duke: You need to keep sending something but if you're limited
you only have PING and PADDING. We set a timer for the client when
there's not outstanding data since we need to drive the handshake
forward, this seems simpler.

Lars: There's a bar for changes here, is there enough interest to make
it happen / do we want to work out the potential security issues raised
by Kazuho?

Jana: Right now, our implementation and many of them don't tie what is
sent on PTO to the event itself.

Ian: If you arm the timer today, you spin loop and that's quite bad. So
this is moving an if statement and not creating a new special case.

Mike: To restate, today when a PTO fires you're guaranteed to be out of
the anti-amplification phase then you can ignore if you were in this
case, since otherwise you wouldn't have armed it in the first place. Now
we'd be moving the check to after PTO fires instead of before.

Eric K: Do we think the mechanism is valuable?\
Kazuho: I've already raised my issues, performance, etc.

Ian: I'm not seeing a lot of interest in taking this up, happy to work
through the performance issues if anyone wants.

Jana: I'd also be worried that there would be further side effects to
get it sorted out.

Ian: And for the first set of this, there were four tries and that was
painful.

Martin Duke: I think there's a deadlock in the current PR, so it's
definitely possible to get this wrong.

Proposal: Ian to decide if he wants to pursue this, and close or group
people to solve the issues

#### [\#3335 Immediate retransmission upon loss detection](https://github.com/quicwg/base-drafts/issues/3335)

Ian: Just need to write a PR, resolution is in the issue.

MT: To summarize: Send a packet with stuff in it when you get a loss.

Ian: Sending exactly one packet when entering recovery matches with
currently specified behavior for TCP, we cite that.

#### [\#3078 Lost Server Initial Takes Too Long to be Retransmitted](https://github.com/quicwg/base-drafts/issues/3078)

Ian: This has outstanding PR that has a bunch of comments. Don't need to
discuss right now.

Proposal: Ian to continue to update the PR based on the comments.

#### [\#3094 congestion window increase on every ACKed packet could result in bursty sends](https://github.com/quicwg/base-drafts/issues/3094)

Jana: We've been back and forth on this. Limiting of sending data on an
acknowledgement with pacing is gone, we're not going to try to recommend
anything there. Latest iteration is that we

Eric K: \<words\>a) If you don't pace do this really simple pacing
thing, b) if you

Ekr: Server's going to do whatever the server's going to do

Roberto: Rate means that you get to choose the denominator. We not being
clear on what the hell we're pacing in the first place. Most of the
problems come around packet based rate. Such a distinction could be
useful for people here.

Ekr: It's very hard to write normative text here.

Lars: Is there enough of a problem that we think it would be bad if we
didn't make a change to the spec? Lots of people are already not
actually implementing recovery.

Ian: Recovery has a bigger piece around loss detection. Don't really
expect anyone to ship Reno. We are implementing the rest of the draft.

We go where we are today because there are some implementations that
really don't want to require pacing (Microsoft being a notable holdout).
Slowstart after idle is also widely unused and we don't want to require
it since that just makes it seems like we have our heads in the sand.
The 10 packet burst was a compromise because we can't make it a MUST if
Windows is not going to do it.

Jana: On the issue of bursting, we don't have anything that says a
strong recommendation about timing, I'd consider even removing that. We
don't say exactly what pacing means, either. Saying you SHOULD do
something but we're not going to tell you what is not great for
implementers. I absolutely expect people to implement Reno, Cubic is not
necessary, Reno is completely reasonable and fine. Netflix still uses
Reno. I'm not arguing that policy here, but I don't want to give the
impression that nobody will implement that.

Mirja: I'm wondering how much normative language we want to use. The
point about the ten packets was saying if you go to send more than 10
packets, don't until the next time you wake up, either timer or new
packet based.

Jana: Would it be reasonable to say MUST pace and say that there's a
minimal option.

Lars: Say this is written with the assumption that you pace and say that
the congestion control part of Recovery won't work for you if you don't
pace. If you implement it, you MUST pace.

Matt: If they're not implementing it, then they're not going to follow
it anyway.

Ted: If you're going to say that, are you also going to say "it won't
necessarily work for the network, so you MUST have some other strategy
to make sure that you don't hurt TCP or other flows on the network"

Martin T: We cite 8085 for that purpose right now. We say you need
something in this space.

Ekr: Is this factual or normative?

Eric K: None of congestion control is super enforceable, do we just say
"MUST pace" and keep the reference to 8085 to cover the other cases.

Jana: So we can say just "MUST pace"

Eric K: Do we also say "here's the most basic pacer you could do"

Rui: I like the idea of specifying the most simple thing, this follows
the same as we do for congestion control

Ian: Adding more detail about what pacing means would be valuable, and
that's been requested before and would be good.

Jana: I think the equation is good, it's much more concrete

Martin T: This is helpful to put in more detail on what this means

Proposal: Require and define pacing.

#### [\#3259 Safety issue during incipient persistent congestion episode](https://github.com/quicwg/base-drafts/issues/3259)

Ian: RTO in TCP is implemented by temporarily modulating the congestion
window temporarily, PTO in QUIC does not do that and so you don't need
to declare all in-flight packets as lost. This means that it's possible
to have new congestion window space available and you could send new
data in addition to PTO. This is a slight difference from TCP, but the
argument is that it's strictly less aggressive than a sender would be if
it were to fully utilize the link. Substantially so, since you're not
spreading the entire window over RTT + PTO. I can write editorial text
to point out that this is a slight difference and why it's going to be
okay.

Eric K: I think we've been trying to keep closely to TCP's behavior, but
in a case where QUIC's design results in a difference like this we
should just have editorial text that acknowledges that and explains why
it's not a problem.

Proposal: Ian to send editorial PR with some details

#### [\#3272 pto\_count should be reset when dropping a packet number space](https://github.com/quicwg/base-drafts/issues/3272)

Ian: Wrote a small PR for this last night, it's one sentence. You should
reset PTO and loss detection timer when discarding keys because it
indicates that you are making forward progress, so it makes sense even
if you didn't get an ack for some reason. You need loss detection timer
because if you don't you might end up in a place where you're in the
wrong packet number space when it fires. I can add the pseudocode if
anyone really wants, or someone else can.

Lars: Pseudocode should mirror the text, but a comment might be enough
here

Ian: No pseudocode yet for any of this part (dropping them), so if we
want to add that, we should add them all.

Martin T: That's stuff that's easy to get wrong, so we should be writing
it down

Proposal: Ian to add pseudocode to existing PR, otherwise ready to go

#### [\#253 HTTP/QUIC without Alt-Svc](https://github.com/quicwg/base-drafts/issues/253)

Mike: Pending HTTP Core text that Roy has in a PR right now that
describes how you decide what server endpoint you think might be
authoritative for a given request. That got written a while ago, it was
updated recently. Once that lands we can point to it and update our text
to match.

Proposal: Wait for the external dependency, should be soon.

#### [\#2223 When can you coalesce connections](https://github.com/quicwg/base-drafts/issues/2223)

Mike: Same as the one above, waiting on external dependency

#### [\#3423 active\_connection\_id\_limit is unknown for 0-RTT](https://github.com/quicwg/base-drafts/issues/3423)

Marten S: We don't remember the limit for 0-RTT since the server doesn't
store it in the session ticket, so the client can't really send a NCID
frame since it doesn't know if it's going to go paste the limit.

Kazuho: We say a server can ignore 0-RTT and that the client can
remember it and retransmit them in 1-RTT if the server rejects 0-RTT. In
that case, the server is never guaranteed to remember the previous
limit.

Marten S: I don't think it's valid to just retransmit in case it's
rejected, because other parameters may have changed

Eric K: Can we just ban NCID and RCID from 0-RTT?

Martin T: I would object to that, why do we need to do that?

Marten S: The problem is not what happens if 0-RTT is rejected, the
problem is what happens if it's accepted.

Martin T: It's the same as all of the other things. If we need to
remember it, then we should remember it.

Marten S: This isn't required to make 0-RTT work, though, and we only
remember those.

Ian: On retire connection ID that one just doesn't make sense

Ekr: I've heard two proposals: ban these and remember them, anything
else?

Roberto: The server would ignore and communicate that error

Lars: You don't need to remember the TPs unless required to make 0-RTT
work, but if this can make an error then it by definition is required to
make 0-RTT work.

Victor: Instead of banning them, assume the default value for 0-RTT and
move on.

Nick: What's the use case for doing this?

Christian: Default value is actually 2

Kazuho: Problem with using the default value is that the server needs to
support providing new connection IDs

Ekr: I don't think this is substantially harder to remember, most
servers have a configuration ID and it doesn't necessarily create ticket
bloat

Eric K: Ban or remember

Roberto: Retry without using the 0-RTT handshake?

Christian: Based on the discussion it seems that just banning them would
be much simpler

Mike: Not only is the default value 2 and it must be no less than 2. If
the client assumes the default value is 2 then it cannot accidentally
exceed the limit.

Marten S: 0-RTT packets don't let you know what server CID will be used,
so you don't know if it's of length 0 or not, so you don't have a real
default.

Ekr: We will have to fix the TLS draft if we allow them, since TLS
currently says that's not allowed.

Ian: To Marten S's point, if you don't know the default and sending
something and then later realizing that you've violated the limit seems
super weird.

#### [\#3413 Does the amplification limit apply to PTO packets?](https://github.com/quicwg/base-drafts/issues/3413)

Most of the room: Yes

Ian: This is true from the existing text, do we need to clarify. There
is text that says if you hit the amplification factor then you MUST not
arm the PTO alarm.

Jana: Ekr made a good point, if the PTO alarm was already alarmed if you
hit the limit. We might want to say shut down the timer.

Ian: The problem is worse if you receive a packet if it's not armed, we
need to have text that clarifies. Still editorial.

Proposal: Editorial

#### [\#3420 Forced connection ID retirement](https://github.com/quicwg/base-drafts/issues/3420)

Kazuho: It doesn't seem correct to argue that the only use case of
retiring a connection ID is when the server issues a connection ID
specific to a path.

Martin T: That is wrong in the text, we clarified that at lunchtime. But
the rest of the argument still holds.

Martin T: It would be a simplification to the connection ID protocol
that we've got so far.

Mike: Yes it would be

Ted: The point that someone was making about the encryption state is
interesting, but the reason that we started down this path a long time
ago was to make hints to people that they didn't carry a CID across a
path change to establish linkability. We already decided this.

Eric K: But we already say no CID sharing paths, but that's not the most
important part.

Ekr: The proposal is that you'd want to go back to needing to remember
things forever.

Roberto: The best that we can do is request it and take action if they
don't do what you want.

Ian: Given where we are we should keep this and recognize that it's not
really a requirement, it's kind of best effort. It is useful in some
circumstances. Nick pointed out a good use case, which is that NIC-level
packet steering by CID you might want to be using this. That's pretty
relevant even if detailed.

Mike: We waffled at the time about whether it would be a should or a
must. The server is informing the client that at some point in the
future these CIDs might not be valid. If you try to use them after they
go away, you'll lose your connection.

Ian: This is similar to STOP\_SENDING, enforcing this and that would
both require tracking acknowledgements of frames

Jana: Honestly, most people will have a fixed time because the device
that's stopping using the CID is running on a fixed time.

Martin T: I want to get rid of all those times, but it's going to be
painful if we do so.

Igor: Client do it quickly, server be generous

Roberto: Server stop respecting it as quickly as is reasonable?

Mike: We need to keep the distinction between RPT and RCID

Martin T: And once you've gotten RCID you can be sure the other side
won't blow up if we get a stateless reset, so it's safe to do so.

Jana: I think we're moving towards some different text, the most clear
piece is take out the 3-PTO that says you don't know until the RCID
frame is received, and if you run out of time to wait then you've run
out and it's on the client to have retired it sooner.

For the client we say "stop sending as soon as is reasonably possible".

Mike: Still nice to say "don't drop it sooner than X, but you drop it
when you drop it"

Martin T: You might keep the CID live for some period of time to account
for reordering and delayed packets.

Jana: I'm not really expecting implementations to be able to follow
3-PTO because there's some external box that has its own time where
it'll stop working.

Mike: My recollection is that Nick can plumb some state but you want to
be able to bound the time on that state.

Eric K: Do we do this as editorial or are we still thinking about the
MUST?

Jana: I think we're talking about the MUST

Kazuho: It's not really about sending RCID, but rather acking the NCID
frame that contained RPT. I agree that a SHOULD or otherwise you might
lose your connection.

Ted: It's a description of the consequence, if we agree on the
consequence (i.e. that if you don't do it you'll lose the connection).
Vote for just making editorial.

Jana: MAY 3-PTO, does that need to change?

Mike: We're now saying that is a statement of fact that it could happen
and we're recommending that we try and keep it around for a while.

Proposal: PR that clarifies the consequences for both sides on what
happens when an endpoint sends NCID with RPT and the receiver does not
retire the CID. Remove PTO mentions from the text around this process.

#### [\#3408 Is absence of both :authority and Host an error?](https://github.com/quicwg/base-drafts/issues/3408)

Mike: We say in HTTP/2 that if you're going to make HTTP/2 directly you
should use :authority instead of Host, but if you're translating an
HTTP/1.1 request into HTTP/2 you leave the Host header and that's fine.
HTTP/1.1 requires a value for Host and if you're doing HTTP/1.0 or
earlier and don't have one, you put an empty one. HTTP/2 doesn't say
anything about what to do if you're translating something pre-HTTP/1.1
into HTTP/2. HTTP/3 doesn't say anything about what happens if you have
neither.

Mark: HTTP/1.0 you can use the Host header, and everyone does. HTTP/0.9
is deprecated, so we don't have to worry about that.

Martin T: You don't.

Mark: The most straightforward thing to do is to copy HTTP/2 into HTTP/3
for uniformity. There are some concerns around if I don't have to change
stuff when I translate, but HTTP/1.1 could just copy buffers and HTTP/2
or HTTP/3 can have sadness

Mike: Absence of either is not an error right now.\
Roy: There's no reason to. The reason that you need an empty Host if
there isn't one, IESG required that you must always send Host in
HTTP/1.1 even though it wasn't necessary. In HTTP/2 that requirement
disappears. What you do need is to say that if there's no Host and no
:authority, then that component is empty, and there are many forms of
URLs that do not contain an authority component.

Mark: Can you translate an HTTP request with an http scheme with no
:authority or Host

Roy: Indeed, no, and you'd have nowhere to route it to

Mike: The one section on URI talks about using heuristics to determine
what that value should be

Roy: Remove the heuristics

Mike: That's in HTTP Core, you want an issue?\
Roy: Yes

Mike: So if the scheme says it's required, then it has to be there, and
remove heuristics from Core.

Roberto: Should we say that HTTP/0.9 can't be converted here?

Proposal: If URI scheme has a mandatory authority component, then you
must have one of these two things, ideally an authority, and pick up the
HTTP/2 text aside from that. File issue on Core to remove heuristics.

#### [\#3418 Order transport parameters](https://github.com/quicwg/base-drafts/issues/3418)

Marten S: What the issue says. Two advantages: First we are slightly
reducing fingerprinting surface, but questionable if that helps in
practice. Second, it allows us to enforce the requirement that each is
only sent once, currently it's a MAY check because it could be hard to
enforce. If ordered, it's trivial to check that.

Kazuho: IIRC, the only reason to choose MAY is because it was hard to
validate, so if it's in order then it's easy to validate. Reduces
complexity.

Mike: Increases the odds of having to conform.

Ekr: Seems like an unnecessary change and that's trivial. This is super
annoying to check.

David: I'll add that in the Google implementation we already do this
because we had to encode them in an order and that seemed like the most
obvious order to put them in, and it would make things easier, so I'm in
support.

Lars: I actively randomize them at the moment, so take that.

Roberto: If someone erroneously duplicates them and they differ (see:
HTTP headers), it becomes unclear which code is going to access which
duplicate, and it becomes hard to interop. From an interop standpoint,
ordering them so you can guarantee that people won't do dumb stuff is a
good thing.

\<Didn't see who said this\>: HTTP/3 SETTINGS as well?

Ted: "While we're changing stuff" is kind of a slippery slope, this
doesn't seem to be worth it to me.

Martin T: We don't do this in TLS and it turned out to be useful to not
have it, and it doesn't make it easier to fingerprint. In TLS we found
that we needed to put something at the end (PSK blender) and it had to
be at the end. Only increases the fingerprinting surface if the order is
dependent on some way if it is dependent on personal information, not
valuable to make it hard to tell which stack is in use.

Jana: Had not considered having some structural requirements, to me that
doesn't seem like a good design.

Ekr: Wasn't good, just ended up that way.

Jana: I think the problem comes up because of the design that we have,
we could have done it before.

Andy: If you put them in reverse order, that would allow you to have an
extension that changed how you'd parse the TPs that were defined before
that document.

Ian: I'm generally in support because we've seen minor issues in this
area before, but it doesn't matter that much.

Kazuho: Regarding Martin T's about TLS's design, the only reason we had
to do that was because the client hello had to be compatible with TLS
1.2

Martin T: This is constraining us in a way that might be awkward in the
future, not quite what you're saying

Kazuho: QUIC is upgradeable, and the current design gets really screwed
up, I don't see any reason to require them to be unordered.

Martin T: How many people here are not checking for duplicates?

\<A few hands go up \~5\>

Dmitri: Anything we don't know about we don't check, but if we know
about it we check

Martin D: There's no harm on checking ones that you're throwing away,
right?\
Martin T: Yes, I think we've already agreed to that

Matt: Yes, and you're only looking at a small number of them

Proposal: Close with no action

## Thursday 6 February

### Zombie Issues

#### [\#3353 Description of Preferred address CID](https://github.com/quicwg/base-drafts/issues/3353)

Mike Bishop: While there might be some more complicated things we could
do. Since most of the endpoints are the server (if you have split brain
it's on you) these servers can coordinate to make them interpretable.
What we like to see on approach outlined, but for the protocol draft we
don't need to do split brain. If after you've migrated, if you want more
you can do that too, but that's not something we need to put it in the
spec.

Lars: the set of valid CIDs must be valid for all addresses you could
use.

Jana: This is one solution. It's not a protocol problem.

Eric K; No change to core docs, and maybe a PR for the LB draft.

Martin D: Not sure we need to LB rev the draft,

Mike/Jana: Maybe we should.

Mike Bishop: Might need an AI to address Kazuho's original question in
the issue. Might need some text that says yes or no.

Lars: I could also get a preferred address. Close and reopen to new
port.

Ekr: why would you assume that would work.

Mike Bishop: You could also get a retry token, but you loose...

Igor: You continue your connection, but you use a new address.

Lars: Thought you could treat this as a redirect.

Igor: It would be a different feature.

Eric K: We can't stop you from using a new address.

Martin T: This is not alt srv.

Jana: This could be specific to client or handshake.

Martin D: Submit PR that describes contract ?

Jana: Some clarification it would be useful, but on the CID not so sure.
We might be able to use the same idea for split brain.

Martin T: Say what Kazuho said

Roberto: this is not a design issue, but there may be an editorial
change.

Martin D: there might be stacking on top of LBs. As I said I'm not clear
that's the right solution. We may need to relook at max CID value.

Lars: see Issue tl;dr: close no action.

#### [\#3428 H3 guidance on CONNECTION\_CLOSE does make clear if the type is 0x1c or 0x1d](https://github.com/quicwg/base-drafts/issues/3428)

Mike B: this should be editorial

Martin T: isn't this up to the transport stack to close for other
reason?

Lars: Editorial

#### [\#3427 active\_connection\_id\_limit description is unclear about whose connection ID might be zero length](https://github.com/quicwg/base-drafts/issues/3427)

Nick: This might be editorial

Martin T: The design issue is to have a safely fixed transport
parameters. In this case it would remove the server's safe behavior.

Kazuho: The server might change the CID

Martin T: This comes back to "remembering"

Mike B: On that issue, I put yesterday what we discussed at dinner about
why the current text has all the right rules it's just that the lines
are not drawn.

Lars: This one is editorial. Martin T to submit new design issue.

#### [\#3423 active\_connection\_id\_limit is unknown for 0-RTT](https://github.com/quicwg/base-drafts/issues/3423)

Mike B: the current has all the right bits for how to use current CID.
See text in issue :) (many thanks)

Kazuho: sending a reiured frame in O-RTT. Is it a protocol Violation?

Mike B: Yes

Igor: What about CID with server preferred address?

Mike B: Could you ...

Igor: Can you switch to the middle of it in 0-RTT?

Christian: I hear your reasoning, but we have two simpler solutions: 1)
leave as is, 2) ... Your solutions means we have to count that harder.

Mike B: It's two until the server tells you otherwise.

Christian: Can we just say nah don't do it.

Marten: We don't have a value before anything is set. We only need
default if the peer does not set the value.

Mike B: There might be some text about using 0-RTT and then do what

ekr: not persuaded by argument on screen. Yesterday we had four options
- none of them work perfectly, but how do we get out of this?

Martin T: we are relitigating about the prohibition of certain frame
types in 0-RTT. Then we decided to treat 0-RTT and 1-RTT because certain
frames wouldn't be present.

Ekr: Are we prevented from sending these frames? Nothing prevents me.
You could say that the rules permit not sending them to end up in error
case. Or, it's nuts to send them.

David: I understand the point about 0-RTT vs 1-RTT there be dragons.
There are different security properties.

Martin T: Now we are relitigating. We ended up spinning our wheels on
flow control ids.

Jana: We should expect that some packets don't get sent. If they get
sent you end up in a strange state.

Roberto: +1

ekr: proposing "it is not safe to send connection ID in 0rtt"

Roberto: Trying to be factual

ekr: general assumption that you can send data in 0rtt, and there are
things that are clearly erroneous. there is a middle space\...

Martin T: That statement is still conditional of forgetting the
numbering space

Brian T: I like the middle space. But, the size of that space depends on
the assumption about the other peer's assumptions. I prefer this be an
editorial fix.

Marten: I would be happy with Mike's solution. I do not want to allow
something that is unsafe. We should be clear aout what happens if you
get it.

ekr: the spec is not entirely clear. the only conditions under which
it's safe for the client to send three CIDs is if it thinks the server
can remember four. we need to make that clear.

Mike B: if not valid, can the client assume the default. (reads text)
"the client MUST use new values, absent thatm, must use default".

Martin D: If the seq are forever out of synch?

Mike B: In what state would the server forget?

Martin T: You can't ignore stuff.

Martin D: That's not what I heard in this discussion. Send in CID packet
and well something might happen or not.

ekr: I read MT's point as larger not that he cares about the CID in the
handshake?

Jana: we need to be clear in the spec.

Mike/Jana: we need the spec to be clear.

Martin T: Got PR. Bigger question is whether the transport parameters
need to be remembered. We're very selective now about requirements. We
should be less selective here.

Marten: The principle is that we save what we need to send data and
NOTHING else. It's less data and if the server changes one of the
parameters then o-RTT gets rejected.

Martin D: We only want the server to respect certain parameters. (ekr
just needs to retain config)

Roberto: My understanding is that you can put connection close in 0-RTT.
How is that different.

Martin D: You might.

Roberto: Why would you do this?

folks: ....

Ian: I like the idea of the principle that 0-RTT should not include
forbidden things. I also pefer to remember fewer parameters. Ones I
include I can't change. This impacts 0-RTT.

Mike B: It's reasonable to include CID?

Martin T: Looking at set of transport parameters, there are a couple
that make sense to change with complete impunity. e.g. max ack delay. We
don't require people remember max packet size. The default posture is
safer. Remember this except in 0-RTT you skip x, y, z.

Brian: As I understood the logic: 1) a lot of 0-RTT rebinding will use
different path (so no need to reuse it), 2) reduce the amount of state
you've got. (Probably safe to over-remember and adjust in any case).

ekr: on client, ok, you're storing cert chain anyway so who cares.
adding more state at the server is also not a problem because you'll
store configurations, not path properties. What falls between the two
stances? There's a push towards stopping the client not changing things.

Martin D: We've generalized this discussion. Maybe we have a PR instead
of doing this on the fly. Four options; remember transport, comply with
default, ban NCID, say nothing,

Jana: I like the idea of narrowing the scope. Let's solve problems that
are causing us pain.

Marten: Regarding the remembering if we do more then we need to consider
extensions.

David: We already got text that says extensions need to define when they
need to be remembered.

Martin D: five options:

1.  No NCID in 0-RTT

2.  Must remember TP

3.  Assume default max\_conn\_id = 2

4.  Assume max\_conn\_id=0

5.  Keep it ambiguous (or explicitly undefined)

Christian: If set parameter to zero that means the server cannot send
them in the preferred address parameter.

Lars: what do you prefer:

1.  Ban = 9ish

2.  Remember = 5

3.  3

4.  0

5.  0

Mnot: Can anybody not live with \#1?

Jana: This is the first one we're banning.

Martin T: Dmitry's point is that it will be harder to implement. And, I
agree for me.

Brian: Different for generation and reception?

Jana: The client might violate them. We always assumed it was 2 or 3.
Why are we even talking about 1?

Ian: max\_conn\_id=1 is the right solution.

Marten: 1 is really weird. Can only send a new connection ID after
retirement. Client can't initiate migration

Roberto/Mike B: Two actually includes 1 - for the client.

Lars: There are three options.

Martin D: we're down to three: 1=1, 2=10, 3=6. 1 is gone, Dmitri, you
going to die on this hill?

Dmitri: I refuse to die. \[applause\]

Martin D: If I was a client and didn't remember the RP how is this
observable?

Martin T: we need to fix that.

Marten: We need a principled approach.

Martin D: Is going to argue there is no functional difference.

Mike B: I do not see anything that says you are allowed to use the
default until you see the TPs. I think you have to remember for 0-RTT.

Igor: there is a difference for the server.

Igor; 2 might be easier for clients, but harder for servers.

Ian: That is the big difference.

Nick: Yep and there might be some more 0-RTT rejects. Not many use cases
for sending NCID in 0-RTT so just assuming the default is less work
overall.

Ekr: see 18.2:

Roberto: supports 2.

Christian: I don't like 2 and prefer 1. I would rather have the safety
of not sending a CID until the handshake is done.

ekr: Still confused.

Martin T: What are the principles?

Lars: We should not fool ourselves. "Principles" and "QUIC" is an
interesting juxtaposition.

Martin D: I was in 3 but have moved to 2. 2 seems cleaner.

Marten: I am easily convinced, but I need to know what they are.

Martin D: There is no other default for TPs.

Discussed backporting principles to fit 2 (server remember it because
the client might screw it up)...

Lars: between 2 and 3: 2=\>12, 3=\>1. We will send out PR\#3425 for
consensus.

### Extension Drafts

#### Version Negotiation

David/ekr: we are planning to submit this draft once we get WG chair go
ahead.

David: Questions?

Martin T: How much progress?

David: None.

Martin D: Add it to the interop matrix?

David: Add it to hackathon in Vancouver. Most feedback is on framing
(i.e., editorial). I think it's ready to be implemented.

#### QUIC-LB Update

Martin D: No slides

Mnot: thanks

Martin D: I hacked datatracker :)

Martin D: If anyone is ready to fire an issue send it to personal GH
repo.

Lars: Each draft gets its own repo.

Martin D: I will create some test parameters.

Martin T: That is good.

Martin D: Going to contact some cloud people and get them hooked in.

Martin T: Big question: you have a number of ways of constructing CIDs.
Should it be a bigger or smaller set.

Martin D: Yep. The team was large and that's why we ended up with them.

Martin T: Might help to have guidelines for the properties you get out
of them.

Jana: I like that recording the principles is important.

Martin D: Retry might change with each QUIC version.

#### Datagram

Eric K: Looks like it used to.

David: We got a lot more feedback and we've done more revisions. Did
another review so I think it's ready for interop.

Lucas: Slideck has a datagram and a h3 datagram. Let's people test
without lots of extra stuff.

Eric K: Basic echo test is what we are looking for in interop matrix.

Lucas: Should we put extension on interop matrix

ekr: Not worried about the letters. Darkness is what people are looking
for conformance. Adding more means less dark.

spt: wasn't the summary that we aren't where we need to be?

Igor: two different things: how dark is your green and the matrix is
good for who else did it.

Jana: Do we want to spend time discussing how to present this?

Lars: we could add a line for adopted extensions

Lucas: Can we have sep matrix for extensions?

Lars: Don't use green!

Lucas: I will take that on!

#### [Ack Frequency Extension](https://github.com/quicwg/wg-materials/blob/master/interim-20-02/ack-frequency.pdf)

Jana:
\[[slides](https://github.com/quicwg/wg-materials/blob/master/interim-20-02/ack-frequency.pdf)\]

Ian: Have seen this in the wild, without ack freq reduction, CPU
constraint means ack-per-2 halves the throughput.

Jana: There is a tension between the server wanting to send more packets
and the client not wanting to receive them.

Martin T: IF you're making a connection in the datacenter and one that
is elsewhere with the same TPs, the settings might not work that well.

Ian: There are some cases where these works and others that won't,
specifically app-limited, small-packet workloads.

Ted (on slide 7): what do you mean about tolerance? Why does one side
have a tolerance and the other does not?

Christian: \[reverb and lowpass\]....

Jana: When I use the word tolerance I am mostly thinking about the
congestion controller. More acks you send and this hurts the congestion
controller.

Matt: you can signal this both ways.

Ted: Not sure tolerance is the right word.

Jana: We can discuss that later.

Lars Slide 10: I would just rename it to ...

Ted: Not sure this is really about tolerance. If it's about throughput
...

Matt: this is fundamentally a one way signal

Jana: Only negotiate for the direction of the data.

Martin D: Should this have an impact on sender ack?

Matt: this sets that policy

Martin D: This is advisory?

Jana: In that case this is not advisory.

Jana: If you get 'em in a batch, you can still ack them as a batch

Roberto: A lot of these things can be expressed as rates. Ignore seems
like one of those things; if I'm rate limiting OOO things, that might be
a longer rate. Consider a more normalized approach for ignore.

Martin D: This is important and we should do it

#### [Multipath Extensions for QUIC](https://github.com/quicwg/wg-materials/blob/master/interim-20-02/multipath_extensions_for_quic.pdf)

Quentin De Coninck: see slides

Ian: you mentioned data prioritization, neither H3 or QUIC have this.
did you add this locally? is it necessary to change the API to make this
useful

Q: e.g. wifi versus cellular

Ian: does MP imply we need prio?

Roberto: sorry, no good answer. This is a fun space in terms of
problems. it squares number of schedule things to describe. how does
this bubble up to the layer above? we're talking about mechanism. We
really need to focus on the connection to the layer above.

Viktor: I am just extending what Roberto said - there\'s a lot of fun
things to do.

Martin D: Is the 5G decision still open?

Quentin: They wanted it now!

spt: Can we ask Gonzalo?

Mirja: In 3GPP, this is a study so far, It will be coming up shortly.

Christian: I like this work a lot. But, it comes fully packaged
.Difficult for apps to make tradeoffs here. We should break this
proposal up into different pieces.

Brian T: How does this new address ID work? We might need something
ICE-like. (winces) Echo - Roberto/Viktor - there's a lot of work here.
Maybe it needs its own WG? (winces harder)

Lars: Don't want to spin the work out of the WG.

Omar: Is this optimizing for throughput and resilience trading off
strict ordering?

Quentin: This is something that the control should take care of.

Jana: I think we should reframe some of the conversation: we ought to be
asking what problems we want to solve. We don't have a problem statement
- if that's the case then we need an RG. Need a real scheduler, etc.

Eric K: What I see as the different questions are: 1) Do we want this
and what are trying to solve, 2) if we want it where do we do it, 3) how
do we do it? Split audience for mptcp cause some problems

Roberto: Reacting to something Lars said - it is so expansive in the
things it touches. It might touch HTTP. This effort might touch more
than just transport.

Lars: There\'s a way to do MP without letting the app know about it.

Ian: Viktor rightly pointed out that an API should provide
prioritization. That problem is sovled. Echoing points Jana and others.

Brian: Clarifying advertisement: there is an existing research group
looking into the path properties part of this. Come to PANRG. We also
have work on how to bind properties to messages in a transport API in
TAPS. Neither of these need to be bound to a QUIC implementation of MP.
Echoing: MP work in the past reacted to network dynamics, not
application needs. Need to think about both.

Lars: MPTCP didn't need to think about the application because it was a
workaround for TCP. Here the problem is much wider.

Jana: MPTCP not having an app driving it was an issue later. Without an
application you won't have a scheduler. Apple solved it for Siri in a
particular way. Without a scheduler it won't work.

Gorry via Tom Jones via jabber: \... my point is similar to Jana\'s: The
states problems could be mitigated by mulipath-failover (which is
tractable and we have experience); if we are talking about cases where
we need to share capacity between heterogenous paths, I would like to
understand why it is useful to use two paths at the same instant in time
for the same flow, and then understand the technical challenges when
something like QUIC tries to do this, and whether the App needs to be
involved in the tradeoffs; how this impacts CC; and other aspects.

#### [QUIC Loss Bits](https://github.com/quicwg/wg-materials/blob/master/interim-20-02/loss_bits_extension.pdf)

Igor: See slides

Igor (slide 2): authenticated not encrypted.

Marten: Loss detection and recovery in our spec is only advisory.

Igor: When you decide the packet is lost, you increment the counter.

Marten: This is an implementation decision.

Igor: Yes, when you decide it's lost you increment the counter.

Marten: So the network needs to know your algorithm.

Igor: No, the assumption is that if the sender thinks it's lost, then
it's lost.

Lars: Move forward on that assumption plz

Martin D (slide ?): Is N (for Q bit) a global parameter?

Igor: N is a power of 2, recommendations in draft.

Martin D: Observer needs to measure that and infer?

Igor: Yep.

Lucs: what if they both sent zero

Igor: nada

Roberto: the network is observing and this means that there are more
than two parties involved. Means that unless this is observable, it's
not an extension.

Igor: see privacy, ossification, security slide

Eric K: Same as spin wrt the changing of CID

Igor: No

Roberto: There is a third party who is the target of the information.
WIthout the negotiation of these bits they are ossified.

Lars: 3rd party can observe to know who is using this extension.

Martin D: This might have an impact for future types.

Igor: that would be on the makers of that box.

Mike B: With the spin bit there was experimental that the expected
pattern can be recognized. That is probably true there.

Marten: Concerned this will lead to ossification.

Matt: Seems like this is important if lots of implementations do it.
Weird to have an extension that changes the wire format. Might be the
only one we can have. We should be really careful with this because this
might be the only extension that can do this type of thing.

Igor: everything is about wire format. deployment, becomes useful with
low percentage of deployment. You need to know this to make the Internet
better.

Matt: What's our incentive?

Igor: We talked to them so we know there is a benefit.

Lars: there is some adoption of the spin bit.

Lars: Need some work done by authors to make sure it answers major
questions.

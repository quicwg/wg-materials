# QUIC Virtual Interim on QMux

## Monday, June 2, 2025

(QMux nee QUIC on Streams)

Notetakers: Will Hawkins, Alan Frindell, Marco Munizaga


### Introduction / Administrivia
#### Note Well

This meeting is taking place under the IETF Note Well.

#### Interactivity

Please be interactive and ask questions/contribute.

#### Goal:

We want to make decisions about where to go with the work ...

#### Agenda Bashing

No comments.

### Why QUIC's Stream Model?

Kazuho presenting ...

There are some really powerful semantics of QUIC, but sometimes UDP is _not_ the best transport protocol.

In particular,
- it will very useful when UDP is blocked.
- QUIC is "not a good fit": QUIC assumes transport protocol characteristics (e.g., loss recovery, unreliable delivery, pacing, insecurity, etc.) In other words, QUIC provides many good things but sometimes they are redundant.

As a result, requirements:
- Provide multiplexing (and other "good" things about QUIC)
- Make the minimum amount of assumptions (positive or negative) about the underlying transport protocol.
    - e.g., do not make optimization specific for certain transport protocols
    - do not solve problems specific to certain transport protocols
- Run on any reliable stream transport
- Multiplexed streams to application protocols
- Application protocols could/should map their specific uses of QMux.

### Requirements Discussion/Q&A:

- (Ian S): Prioritization _does_ seem to be important, even though it may not be in QUIC semantics.
- (Ian S): Transport parameters could be a very useful building block/tool to solve myriad problems (Lucas +1)
- (Ian S): Default mapping between applications and QMux "configuration" (ALPN).
- (Ian S): Is the only way to identify QMux as the application protocol the ALPN? Based on experience from MoQ, ALPN was a useful tool.
    - (Lucas): Not necessarily. It could be, but there are other ways to do it.
    - (Lucas): See applicability document for more information.
    - (Kazuho): Agrees (generally) But, there could be places where you can assume ALPN-like parameters and an actual ALPN would be wasteful.
- (Victor): QMux is like WebTransport over HTTP/2.
- (Victor): Does it seem like QMux is really the same thing with a different name? Seems onerous on implementers and maintainers.
- (Kazuho): We want to keep kthings separate (have both), as much as possible (and so they might not have _that_ much overlap).
- (Lucas): A lot of complication.  QMux isn't necessarily in a position to replace what webtransport has done.
- There does appear to be some interest in (perhaps) migrating WT/H2 to QMux.
- (Lucas): But, please do not throw away what we already have done!
  - Martin said no to a question around migrating away from WT over h2. Lucas: Migrations are hard, but doable. We could have an rfc...
  - As much of an HTTP fan that I am, a simpler solution could be easier to use.
      -  Having fewer layers of things, improves the success of being able to adapt tooling.
   -  multiplex, flow control is complicated. Would be great to reuse.

Willy: QUIC stream handling and flow control are better than H2
H2 cannot create a stream without an HTTP request, makes encapsulation complex.  QMux avoids this.

Victor: WebTransport is just an API to multiplex streams.  It uses HTTP because that's what we picked.
    - Lucas: Is that a disagreement with the work of QMux?
    This is more of a branding problem

(Lucas): Is there a discussion to be had about whether QMux is _really_ needed?
    - There is a very strong anti-H2 sentiment.

Marco: Is there a future WT over TCP-TLS or unix domain sockets?
Victor: Currently it "works" over anything that is a stream. But, it is branded as H2 because there was no interest in _having_ to work on other protocols.

Ian: Are we talking about splitting WT/H2 to rearchitect and make a better protocol? There might not be that much need to change too much to get this better architecture.

Alan: Feels like there isn't much appetite to redefine webtransport over h2

Lucas: As webtransport co-chair, I do not want to speak authoritatively here. Appetite is to get things done in this group.

Lucas: Responding to general concern that QMux is _just_ WT: There are things in WT/H2 (like Kazuho said earlier) that are overkill and would be wasteful to reimplement.

### Difference Between QMux Goals and WT Goals

Lucas: To riff on the difference of WT and Qmux and have an abstraction that span them, might be difficult. Do people think this would be worthy?

Kazuho: Reliable reset is required by WT. We end up in a infinite wheel of dependencies. Every extension added to QUIC may make sense to add to qmux. While a transport over h2 may not need all these extensions.

The way WT over h2 works is that it sends a CONNECT header and treats the rest as a stream.
And there is multiplexing of WT streams inside that single stream.

There is lots of overlap between WT and QUIC -- in fact, some parts of WT were take from RFC9000.


Ian: Where you saying extensions should bubble up to the qmux layer?

Kazuho: ack frequency does not make sense for qmux because it's related to the underlying data. In the case of WebTransport, it's more about what a transport is expected to provide.

Lucas: Talking about `CONNECT` from experience: Wanted to build a LCD so that it could work in as many places as possible. Basically, "Give me a reliable STREAM and get out of the way."

Lucas: _That_ is the reason that QMux has such a minimal set of "requirements". This decision will improve abstraction and layering. As long as an underlying byte stream is reliable, QMux can work happily and leave application developers to build their best application-level protocol.

Lucas: Let's do a gap analysis between WT standard and the QMux requirements (get vocabulary matched up) and see whether there is a difference.

Marco: If you squint, WT and QMux _do_ look lots alike. So, having an analysis would be good. Could we have a WT spec that works without HTTP?


Lucas: There was a back in the day lightweight webtransport over quic. I don't necessarily want to add work to the WT group

### QUIC WG Patching

We have to patch the QUIC working group charter to allow including this work.

Are we comfortable to allow the QUIC working group to do this by patching the charter?

Kazuho: We agreed we need a generic way to use the QUIC API over reliable byte stream.  There are discussions about how we do that.  We should recharter.

Lucas: As an individual with no hats. Note that we see many +1s in the chat. Curious to hear from folks that disagree. We'll use the next half of this session to see how we can patch it.

Lucas Presenting Slides on Charter Patches

Slide 1: Existing Charter

Recharting process doesn't seem that hard anymore. It should still be generic enough that we don't have milestones in it.

Slide Charter Part 2:

Slide Charter Part 3:
The wg didn't want to be responsible to write foo-over-quic for all foo


Slide would this fit in the first or second work area?:

Martin Duke: You can make a case for the second one. I'm not opposed with recharting to be explicit about the work here rather than trying to fit it into the second one. I would prefer to be explicit. We should not get feedback here when we do a last call.

Marco: are we trying to fit this into the existing charter or not?

Lucas: As an invidual, we'd benefit from adding text to the charter.  Updating the charter will help clarify the scope of work. Even a sentence or two is a worthwhile process.

Ian: Agree.  Is there proposed text?

Slide 4: possible options

Ian: High level comment. If we are having the quic wg work on api surfaces and mappings that work over tcp. That is a fairly substantive change to the charter, and we should be explicit about that change.

Willy Tarreau (on chat):
Maybe when the original charter was written, it was not yet very clear that there were two QUIC layers: transport and multiplexing. It's possible that simply clarifying this point makes any change to the multiplexing layer applicable to any of these two areas after all.

Lucas: doesn't like #2 much.  #3 is more like a milestone.

Kazuho: I like #1, can live with any. I want to echo what Willy said over chat. Two aspects: one is transport the other is multiplexing. We may want to focus on the multiplexing aspect for qmux work rather than a general adapting QUIC strategy.

Victor: 1-3 feel a bit like putting the cart before the horse. We are trying to solve the problem of having applications on the QUIC API on one side and TCP sockets on the other, and we're trying to bridge that gap.

Willy: We may want to sync on what we want to replace h2. Many people, incl me, would like to see h3 in the datacenter. The lack of tcp right now is a show stopper. We want to port QUIC to all the places where TCP is supported and we have use cases, not a generic byte stream substrate.

Lucas: If we define a full replacement of h2 as a goal, it may be overstepping. We'd like to support that work if we can, it may be too lofty of a goal. There doesn't seem to be much appetite of replacing h2 with this kind of work. Instead, let's rephrase as how to we separate these concepts so it becomes clearer how you can adapt these parts to something else. Maybe we need a specific use case of "how we do this over tcp". But that may be concerns around focusing just on TCP.

Martin Duke: 1 or 3 seems better.

Ian Swett: Something that mentions example applications could be better than nothing. Example h3 over tcp using qmux. I don't want to be too specific nor too vague.

Marco: Does anyone have a use case that doesn't involve TCP or IP?

Lucas: aware of some.  Terminate QUIC on a proxy, does some cheap/optimized processing, pass to backend.  Transfer things that are useful.  How do I carry QUIC level information.  Do you level up to HTTP?

Alan: QUIC is separable, not a monolith.  Charter text should reflect this.

Martin Duke: Regarding whetehr we should menetion h2 in the document. The technical work isn't going to need to reference h2, right?

Lucas: We have a document, that describes the multiplexing we want, and what are the things we don't need in this mode. We then have a companion doc that describes how h3 on qmux works. It's more or less: Go read the h3 rfc, this is how the handshake works, and that's it.

Martin Duke: Given that response, the charter should not metnion HTTP. If we want more text we can mention it in passing, but not as a deliverable or focus area.

Willy: the current model has complexity because H2 and H3 are different.  Intermediaries that have QUIC on the front and !QUIC on the back has to implement extensions twice.  Slows extension adoption.  The second area mentions extensions.

Lucas: To explain a bit more with h2/h3 context. H2/h3 have their own frames on top of the underlying frames. Example: Priorities RFC needs to define the priorities frame for both h2 and h3. Codepoint sizes on each stack is different. You need to be able to translate between these two versions.

Ian: We decided to avoid to invest in h2 as much as possible and would like to get rid of it. All modern clients support h3. Traffic is diverging to h1 and h3. QMux is supporting that direction. I'm not sure if that's where others are heading. We're aren't thinking about adding any new extensions to h2. It's risky, and we don't want to.

Lucas: Agree I don't want to. Doesn't mean I can't. I'm in a position where customers are asking for things in h2. If customers did qmux, it would be perfect.

Gorry: AD Hat on. I'd love to see a charter change to make this work happen. And we should run it through the community. I've heard folks talk about TCP and other things. Is Byte Stream the right direction? Is the second point in bullet 3 what we want?

Ian: I don't think we want all of QUIC. "The features and API surface of a typical QUIC implementation exposes". Be clear we're not trying to do congestion control or other QUIC things. RFC 9000 is a huge document. We don't want to pull in the lower layer aspects of it. Are other people interested in the lower bits alone? Acks, loss detection, congestion control, handshake, tls... If you only had datagrams for example.

Marco: There are extensions to QUIC that are not directly related to multiplexing - eg: datagrams?
- We can do stuff besides just multiplexing

Lucas: It's ok to carry datagrams in this model - if we didn't this is a net loss.

Martin Duke: Talk about security. We could do QUIC over tcp "plain text quic". Conversation around how we feel about that.

Kazuho: Operations that an application does makes sense.

Lucas: On the security topic: We depend on the wire image being secure. It helps us build a transport protocol that acts a certain way over the internet. In the initial doc we said you really SHOULD be on a secure substrate. Not sure if we could add normative language here. We could say a "Secure Byte Stream", is that enough?

Martin Duke: We did construct QUIC in such a way that it is hard to run plaintext. We may want to be explicit that plain text quic is not in scope.

Gorry: This is going to get some privacy and security review when we update the charter. QUIC is built on a secure platform. Just saying doing "QUIC over a stream" will open a lot of questions. Can we agree on what we say "encrypted byte stream" "authenticated byte stream"

Lucas: presenting some live-written text.  Authenticated/Encrypted/private etc are too specific and "secure" covers more bases.  We need to mention something about security but this is good feedback from the room.

_word smithing live_

The text will be published on list.

Lucas: _wrapping up_.



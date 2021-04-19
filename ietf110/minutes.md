# QUIC at IETF 110

[Agenda](https://github.com/quicwg/wg-materials/blob/main/ietf110/agenda.md)
Scribes: Robin Marx, Spencer Dawkins
Chairs: 🪑🪑🪑 (Lars Eggert (for the last time), Lucas Pardue, Matt Joras)

## Administrivia - 5 min total

**Lucas**: Welcome to our new chair, Matt Joras!

* Blue sheets
  * Meetecho does the bluesheets
* NOTE WELL
* Agenda bashing

**Magnus Westerlund**: Recharter on agenda?
**Lars**: no, because nothing to do, Proposal is out, no non-editorial suggestions yet. Wait until 18th March.
**Lars**: For those that don't know: Now that we've finished v1, we're changing gear and HTTP/QPACK are handed over to httpbis. We will maintain other documents, as well as operability and manageability and some extensions.
**Lucas**: Core docs are now past IESG (thanks Magnus!). So no issues on those docs today, because they're pretty much done. No more opportunities to open new feature requests/issues if they're not e.g., serious security issues
**Lars**: Talked to RFC editor. Expectation is that first batch goes to AUTH48 in weeks, not months. H3 and QPACK however are waiting for httpbis work, so those won't be part of the initial batch.

## Hackathon / Interop Report
5 min - Recap of interpo at hackathon (interop sheet) - Lars Eggert

**Lars**: Hackathons are less busy than they used to be. Partly because switched to using v1 and not all stacks have made that change. A lot of [interop testing is also happening in an automated fashion](https://interop.seemann.io/) (thanks Marten Seemann) and most of those tests are succeeding.

**Christian Huitema**: Did have perf interop/testing. msquic, lsquic, picoquic, ngtcp2 and quinn did [perf interop organized by Microsoft](https://tools.ietf.org/html/draft-banks-quic-performance-00). Measurements of QUIC performance were done on dedicated hardware. Good news: all achieve speeds between 1-5 Gbps with just software implementations, no hardware assist. Shows two things: a) hackathon is moving from basic interop to performance. b) work done by various OSes to make UDP perform better is starting to pay off. A year ago we'd get 500 Mbps, not Gbps. Especially in Windows and Linux with things like UDP GSO has been paying off.


## WGLC changes to [manageability](https://datatracker.ietf.org/doc/draft-ietf-quic-manageability/) and [applicability](https://datatracker.ietf.org/doc/draft-ietf-quic-applicability/).
[Slides](https://datatracker.ietf.org/meeting/110/materials/slides-110-quic-quic-applicability-and-manageability-wglc-update-00) - *Brian Trammell*

**Gorry**: Not sure we need to talk about priming a CC. If we don't say it, we can still do it and specify in future. If we say it here, need to be careful to explain what it means and that we know what happens if you do this badly and that we give good advice. Not sure we can do last two?

**Brian**: Punting it to the future is a good option.

**Mirja**: Intention is to mention what probe packets can be used for. Not at position where we want to recommend specific mechanism, but still think it's valuable and like to keep it (though without saying more).

**Christian**: Don't think this is ready for primetime. Don't think we have a lot of implementation experience with it, so it's speculative, and would rather not have that in an RFC.

**Gorry**: making it more blunt "assist in determining cc state of a new path" or not hinting at what the mechanism would be, is also a possible solution here

**Mirja**: Could actually just say that: probing packets can be padded with padded data and thus increase CC data, without saying much more

**Brian**: Want to have something here to provide a hint so people don't have to independently re-invent this.

**Mirja**: It's not just internal, since some applications might want to influence how this happens (re: comment in chat)

**Magnus**: Comment on PR 279: simpler if we get previously used draft versions in official IANA registry and then point to that.

**Mirja**: Wasn't there discussion that we -don't- want to do that?

**Magnus**: Some discussion but I don't know, so that's why I want to bring it back up

**Martin Thomson**: getting all versions in the registry should be straightforward. We can then scrap the wiki. In the process of appointing experts for those registries now, should be ready in time for when the docs get published.

**Gorry**: comment on PRs 240 and 178. Still don't know right answers. First one: more to do with environment/deployment context. Willing to help contribute to text for both.

**Brian**: After these issues are merged, we think we're ready on applicability. Have to wait for resolution on changes on manageability to see if we need to issue a new WGLC.

## Open issues, updates to [DATAGRAM](https://datatracker.ietf.org/doc/draft-ietf-quic-datagram/).
[Slides](https://datatracker.ietf.org/meeting/110/materials/slides-110-quic-quic-datagrams-00) - *Tommy Pauly*

**Tommy**: Few [open issues](https://github.com/quicwg/datagram/issues). Targetting shipping in July 2021.

#### [Issue 6](https://github.com/quicwg/datagram/issues/6)
**Tommy**: Propose to add explicit indication why we're not providing a demuxing identifier in this draft.

**Eric Rescorla (ekr)**: not advocating for one or other. Need to specify what benefits and costs are. (Robin: not sure what was said here. Think it's about new applications having to re-define Flow IDs again and again if they use Datagrams, which has a cost in terms of document count)

**Tommy**: Similar discussions about H3 Datagram what these identifiers mean: flow id, application label on set of messages, ...? Puts a bit of burden on app, but also a lot of freedom. Maybe even be that H3 won't strictly use it as flow ID and go broader. This is one of the reasons not to put it in here

**Ekr**: Sure. Can point to H3 Datagram maybe. Say that if you need something similar for something new, that you need to copy that document and adopt it to new use case. If in the future we find the same pattern being repeated, we can suggest that a new extension will be defined with a new frame type that uses that pattern.

**Tommy**: We can highlight that. Looks like H3 will use VLI for this, which is convenient. But up to new extensions to define what that means.

**David Schinazi**: Most use cases for Flow ID seem to be multiplexing applications over QUIC. Intentionally ruled out of scope for QUIC v1. Makes more sense to have it at application layer. Wrt people wanting to re-use this: H3 Datagram doc has 1 section on the flow ID. The rest is about how to integrate with H3 itself. IF another application wants to use this, we don't need to clone and get a fully new document: just need to define what the Flow ID means in their application. No value in centralizing this. Just having each application saying "we also start with a flow id" is the right way to go.

**Tommy**: agree. And just spelling that out seems best.

**Omer Shapira**: In future, if there are more, we might want to provide best practices. But if for now the approach is just 1 integer, then that's probably not needed.

#### [Issue 8](https://github.com/quicwg/datagram/issues/8)
**Martin Thomson**: Not sure why the Loss Recovery PTO is necessary in this case. Is there a succint explanation you can provide?

**Jana Iyengar**: PTO isn't required: it's about what to do when PTO is triggered. Seen this problem before, want to specify how to handle packets you typically don't retransmit. If you want to invoke an ACK, you send a PING frame.

**MT**: This is in recovery, but what benefit does this provide. If you only ever send DGRAMS, what possible value is there. Recovering bytes?

**Jana**: It's mainly for cleanup. Two positions: a) don't do anything if nothing to send, just take conservative stance (e.g., cut back cwnd after some time) b) just send a ping, evoke an ACK, and use that. In transport, we've chosen b) so you can do math correctly. Unless we have a reason not to, let's keep b) here.

**MT**: Makes sense. Slide just looked like new behaviour. So some explanatory text there would help.

**Ian Swett**: If not already referenced, link back to recovery document.

#### [Issue 3](https://github.com/quicwg/datagram/issues/3)
**ekr**: Why would you want to say "I only support DGRAMs of size 0"? Is there another indicator you only support DGRAMS?

**Tommy**: No, no separate one. So this asks if we can switch to a boolean

**ekr**: Saying that you can say you don't support them, but not sending this TP at all. And you can set it to something very large if you don't care. Don't know if there's a reason to say I only support dgrams of size x.

**Tommy**: Main question: does anyone actually intend to use a limited dgram size? For H3 the use cases currently probably don't require, but could be useful down the line maybe?

**David**: To explain reason why 0 means not allowed: to make implementations easier. All of the core spec varint TPs have a default value. Make 0 default here makes that easier: if not received, just set it to 0. Otherwise, you'd need another approach.

**ekr**: Seems that 0 and not present have different semantics? Because TP with value 0 means I support it, but you can't send it, while omission would be "I don't support it". If we change this to only payload, we would lose those semantics, and we would have a new problem. Annoying to take into account other side when you want to send, probably where the idea to change to boolean comes from? Do we have other things that have forbidden minimum values?

**David**: yes. E.g., min payload size cannot be below 1200 bytes.

**ekr**: right, so that would also resolve this: say min value is 1, and default is 0?

**David**: is already deployed. If change this, have to switch TP value, but we have a nice value now, so let's just keep as-is

**Nick Banks**: I never saw good reason to actually have the size limit at all. Would have pref to just have enable/disable boolean TP

#### [Issue 15](https://github.com/quicwg/datagram/issues/15)
**David**: implementation experience. In WebTransport we use DGRAMS and QUIC stack and JavaScript that consumes DGRAMs are not in the same process in Chrome. So application and transport are running separately and no synchronous interface between them. No option for QUIC to wait for async call to app before ACKing the DGRAM (too complex). Proposed resolution of telling implementation: with DGRAMs you don't want inifinite buffers. If app is busy and queue gets too full, we don't want that to grow unboundedly, so you can get loss. But how useful is it to let the app know? What would it do with that?

**Tommy**: At least a way to query "did you drop any packets?", would allow app to do app level signalling (e.g., video streaming with missing frames) to e.g., request retransmission.

**Lucas**: We're at time. cutting queue.

**Nick**: Already have ACK mechanisms at transport. Sad to hear we couldn't leverage that and that application has to build own acks on top of that. For us it was easy to support this, but not for others.

## Open issues, updates to [version negotiation](https://datatracker.ietf.org/doc/draft-ietf-quic-version-negotiation/).
[Slides](https://datatracker.ietf.org/meeting/110/materials/slides-110-quic-quic-version-negotiation-00) - *David Schinazi*

#### [Issue 19](https://github.com/quicwg/version-negotiation/issues/19)
**MT**: I think we need a much simpler design. I realize this is the maximal design. Lot of work to be done on getting transformation between 2 versions working properly. What actually will happen in practice is that a V2 thing that offers a V1 first flight, would have to apply V2 contraints in its V1 flight to enable conversion; nothing in the draft about that

**David**: Something concretely in mind for simpler design? Are there features you could drop to have a simpler design?

**MT**: Version upgrade: typical principle is client offers list, server chooses. For incompatible: you invert that: server offers list, client chooses. That gets us 99% of the way.

**Christopher Wood**: Wonder how much this has been analyzed (i.e., downgrade attacks)

**David**: Has been zero analysis on this, apart from me looking at it, and I'm definitely not a security expert. So yes, before shipping we would definitely want to have folks look at this. reason for adding long header version in here comes from research showing that might be unsafe. Still need to do formal analysis here.

**ekr**: 3 issues. 1) do we actually need all the functionality? (compat and incompat). My opinion is we don't need incompat. 2) is this the right interpretation of compatible? transformable vs valid. In other protocols they are synonyms. e.g., in TLS 1.3 CHello is a valid 1.2 CHello. Is a simpler concept. 3) Given all these functional constraints, is this the simplest design that provides the intended security value? A little unclear if MT is just challenging point 3), but I agree the design overall is too complex.

**David**: Totally agree. Encourage anyone who thinks this is too complicated to propose alternate designs.

**Mike Bishop**: Comes down to what restrictions we intend to put on futue versions of QUIC. If we intend to make it more strict, best hurry, because invariants has already been sent to RFC editor. Problem: invariants say that vneg (Robin: didn't quite follow this). Don't think we have the option to go back on this now, so we can't really toss incompat vneg out anymore. This does make it more complicated, but not sure we can simplify at this point. Path to simplification is to retcon the invariants so implementations need to know about all previous versions.

**David**: Is indeed not always true. GQUIC uses Google Crypto and so we do need incompat for that for example. One thing that comes to mind is splitting into 2 drafts (separate for compat and incompat).

**Christian Huitema**: Strongly in favor of simplification. 1) this is a security feature. There is no such thing as complicated security features 2) it has to be simple. Client should say: I propose A and can also do B and C. If it's more complicated than that, it shouldn't happen. If server wants to say "I also support v42 even though you didn't mention that", that should be a different mechanism.

**Matt Joras**: Clear consensus that we need something simpler. Please suggest concrete designs.


## Open issues, implementation experience, possible WGLC of [QUIC-LB](https://datatracker.ietf.org/doc/draft-ietf-quic-load-balancers).
[Slides](https://datatracker.ietf.org/meeting/110/materials/slides-110-quic-quic-load-balancers-00) - *Martin Duke*

**Benjamin Schwartz**: choose the safest option and get implementation experience with that

**Martin Duke**: we've reached limits of what we can do without implementation (see first extra slide). LB community is not really here, but server community is here. Could really use someone with a server that supports mobility to test with this. Should surface the key use cases. Don't know if we can make a lot more progress on this document without this. Stuck untill we get more reviews and implementation experience. Don't want to go to WGLC without that.

**Benjamin Schwartz**: Also some privacy concerns for some of the options. Some break privacy guarantees that QUIC has previously made. Should be conscious about making recommendations that violate security/privacy promises we made in different documents. Especially because servers and LBs often closely collaborate and generally don't require too much standards guidance. If people want to do something unsafe, they can do so on their own. Mainly concerned about plaintext CID, but also some concerns how it interacts with ECH. In general, for an ECH QUIC implementation with split-mode architecture, it seems like ECH processing needs to be coupled to QUIC-LB handling and seems like relatiely easily to break guarantees of ECH with this.

**Martin Duke**: Can't comment out of hand, but definitely don't want to break ECH. Plaintext CID hsa been in there since start and has lots of support from QUIC community, who are privacy sensitive. Consider this more of a privacy continuum rather than discrete private vs non-private.

## Adoption: [QUIC bit greasing](https://datatracker.ietf.org/doc/draft-thomson-quic-bit-grease/)
[Slides](https://github.com/quicwg/wg-materials/blob/main/ietf108/quic-bit-grease.pdf) *Martin Thomson*

No presentation after some discussion about waiting for recharter and asking for adoption.

## Adoption: [Delayed ACK](https://datatracker.ietf.org/doc/draft-iyengar-quic-delayed-ack)
*Jana Iyengar*

No presentation after some discussion about waiting for recharter and asking for adoption.


## Planning & Wrap up
**Lars**: running out of time. Can't really do a call for adoption of QUIC bit greasing or Delayed ACK at this time anyway, so won't waste time on that (during recharter), but will do so in the future, so please read the drafts. If people have major objections now, please let us know now though.

**Christian Huitema**: What about the timestamp draft? We already have two implementations. Would like some additional visibility of that in the WG

**Lars**: Let put that on the agenda for an interim or 111 then.

**Lars**: Maybe we should do an interim discussion on vneg before 111, since it seems likes it needs more work? (chat indicates interest). Will do Google poll for a meeting slot then.

**Lucas**: There's also qlog that's up for adoption. Drafts are more or less ready, just holding until after recharter.

**Lars**: Logging is indeed mentioned in the new charter as well. That's mainly there because we intend to adopt (part of) qlog here.


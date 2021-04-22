# QUIC 2021-04-21 Interim Meeting Minutes

# IETF QUIC Working Group Interim Meeting

* [Meeting arrangements](arrangements.md)
* [Issues List](https://github.com/quicwg/version-negotiation/issues)
* [Drafts](https://github.com/quicwg/version-negotiation)
* [Chat](xmpp:quic@jabber.ietf.org?join)
* [Minutes](https://codimd.ietf.org/notes-ietf-interim-2021-quic-01-quic#)

See [the arrangements page](arrangements.md) for dial-in information.

## Agenda

### Administrivia - Chairs (5 min)
  * Scribes, Blue Sheets, Note Well
  * Purpose of the meeting
  * Agenda bashing

### Editor's Opening Remarks - David Schinazi / EKR (5 min)

David: Sentiment from last meeting: possibly too complex -- can it be simplified? Let's hear proposals.

Kazuho: Prefer to just define incompatible VN. Do nothing for compatible VN. There are two points of extensibility: VN packets and transport parameters. Compatible VN does not require any work for QUICv1, and we don't know what a future (in)compatible version would look like. So let's do the minimal thing and implement downgrade prevention for incompatible versions in QUICv1. 

Christian: Puzzled by difference between compatible and incompatible VN. Like idea of doing just one. Torn on whether or not we change Long Header verison in the middle of a handshake.

Martin: Added latency caused by incompatible VN might cause problems in deploying new versions. Okay with idea of defining both. Overall design is simple to implement, if not analyze.

David: Why do we want to remove features? (Simplicity, surely.) We need more deployment and implementation experience here. Making things overly simple now may prevent future changes. (Only focusing on compatible may block future incompatible designs, and vice versa.) We need a way to quantify simplicity. 

Kazuho: Not having incompatible VN prevents folks from deploying new versions of QUIC. (Not true for compatible VN.)

Martin: Punting compatible VN could be done quite easily since it's a separable problem. Compatible means making extensions to the core protocol. Incompatible means changing the core protocol meaning (e.g. TLS -> Noise for AKE).

Jana: Feels ignored. Support Martin and Kazuho.

Martin: Can't do everything with extensions. Some changes might require core protocol changes. 

Jana: Can a transport parameter work for V1 -> V2 massaging (compatible versions)? 

Martin: Possibly!

David: Extensions are appropriate for many things (e.g. datagram support). Changing core protocol things, e.g., format of handshake packets, is not appropriate for an extension. VN should NOT replace extensions, but there are things that require VN. Tangent: new versions will help prevent ossification. 

Ryan: Kazuho's suggestion was not to stick with v1 indefinitely and only focus on extensions, but rather to use transport parameters as a mechanism of saying "this is the TP that causes you to switch versions." Retain the ability to have different versions on the wire, but keep the negotiation in the transport parameters. 

David: This is what's in the draft currently.

Christian: If we want to change formats/semantics in significant ways, we need a synchronization point. Before the point we have format foo, after we have format bar. We don't have that many synchronization points. One is version number in packets. Another is 1-RTT packets (?). 

### Opportunity for Opening Remarks (10 min)
  * High-level overview of ideas from commenters on mailing list

(captured above)

### Balance of Time (85 min)

#### Version Negotiation - Watson Ladd (10 min)
  * https://datatracker.ietf.org/meeting/interim-2021-quic-01/materials/slides-interim-2021-quic-01-sessa-versionnegotiation-watsonladd-00

Mike: Rely entirely on transport parameters and client's use of the server's versions. (?missed?)

David: Out-of-band info like HTTPS/Alt-Svc already tells clients version info. We're focusing on other (non-HTTP) protocols. Is this different from what's in the draft?

Watson: Put everything in the client's initial (compatible and incompatible) and expect the server to be able to choose based on that. The server must be able to parse that information for any version. 

Ekr: If the client is wrong in its choice of version for a server, then the design chokes, right? [yes] What does compatible mean?

Watson: Compatible as in TLS with versions listed in an extension. Is TLS a version of compatible or incompatible?

Ekr: Compatible. CHO can be valid for two versions. Incompatible means that the server can't even parse CHO and sends VN. Most of the complexity comes from incompatible version negotiation. 

MT: Does this server-side requirement (always be able to parse version info, regardless of version) require us to change the protocol?

Watson: Don't think we need to change the protocol, but we might need to change the implementation expectations. You might need to implement "enough" of V1 (TLS) to get the version info if you only support V2 (Noise).

MT: Might be able to do this with packet coalescing.

Martin Duke: Not prepared to assume that initials will remain decipherable for all time (beyond invariants, which specify header bits and whatnot). Based on proposal, plain old V1 servers would always send VNs if given newer versions. (Meta: version aliasing draft might be relevant here by making CHO secure.)

Christian: Imagine we had a way to encrypt CHOs -- call it V3. Such clients won't try with previous versions since that defeats the goal of using V3. (This is an example of incompatible VN.) 

David: How is this proposal simpler than what's in the VN draft today?

Watson: There's a bunch of places where we re-encode previous attempts. In my proposal, you encode everything once (with no historical information). 

David: Proposal is not possible because version info is not an invariant. And we can't modify VN packets because of invariants. And so the only way to authenticate that is to stick it in the transcript. (Can this fundamental point be avoided?)

Watson/David: More complex thing is needed because of the invariant constraints. 

Ekr: What problem are we actually trying to solve here? (What do we have consensus on?) Not persuaded by argument that different CHOs (e.g. one encrypted and one not) for incompatible version negotiaton.

Martin: Where do folks stand? Do we want truly incompatible versions?

David: The VN draft has both, and there are good reasons to have both. These could be split into two separate extensions, but they might have the same information at the end of the day. Stalled due to complexity concerns. Are those concerns still valid?

Kazuho: Incompatible VN is inevitable if we anticipate future QUIC versions that don't use TLS (for example). Do we have enough information to design compatible VN now?

Ryan: During the early development of QUIC, there were multiple times where incompatible versions existed. It's conceivable that we may not need to make such changes in the future. But we have an existence proof of it today. 

Jana: (Violently) in favor of incompatible VN. Compatible is a convience, not a necessity. Incompatible lets us agree on how we talk to one another. 

Ekr: Incompatible VN support seems unmotivated. Do we have situation where the client is so unaware of server capabilities that it might have to engage in incompatible VN? (Consider clients connecting to TLS or SSH servers.) ACK Ryan's comment, but was it not true that clients always spoke one version of QUIC? Not persuaded that we need clients to be flexible.

(Chair) Lucas: Are cases that you describe documented somewhere? (Ekr will write it down.)

Christian: Don't believe the VN is too onerous to implement. Agree with David that complexity argument is weak. Would like to have some (best) practices on changing versions in the middle of a connection. Chances for mistakes are high.

Ryan: True that when Chrome was speaking QUIC that it did not exercise VN. It is not true that VN was never used. (Google internal health check tools exercised it.) Sounds like we have rough consensus on incompatible version negotiation. Not necessarily true of compatible version negotiation. Can we get consensus on these problems separately?

David: Expect QUICv2 to look like QUICv1 (and use TLS). Don't foresee a use case where clients debate between TLS-based QUIC and non-TLS-based QUIC. Google QUIC crypto used WebPKI certificates, but was incompatible with TLS. (Chrome supports IETF QUIC and Google QUIC v50, backed by the same PKI, but are incompatible.) We need the option to build something that's not based on TLS.

Ekr: Happy to have both features. Most of the complexity comes from incompatible VN. 

Jana: Seeking clarity on when does one use compatible VN and when does one use TP extension mechanisms? Would appreciate some guidance on this in the draft. Incompatible VN is required for experimentation.

David: Two reasons why we might want compatible VN over extensions. (1) If you have compatible VN, you can start modifying handshake packets (CHO has v1 handshake, SHO has v2 handshake, for example). (2) Using extensions for everything might force us into the TLS model where extensions really change features, rather than versions changing features. Using version negotiation allows the ecosystem to evolve rather than just keep piling onto extensions. 

Ekr: Managing transport parameter buckets is not ideal. We need to avoid that (and hence require compatible VN). 

Jana: Trying to understand what compatible VN gets us compared to a bucket of TPs. If we start with V1 and have to switch to V2 internally, we've ossified on V1. Unclear how compatible VN works in the middle of a connection. ([David]: CHO LH uses V1 and SHO LH uses V2.) Is there value in allowing this feature?

David: Not quite at the point of ossification. We can introduce new versions and aggressively drop old ones once we have enough support for new(er) versions. Big question to answer is whether or not we'll have a real V2 or a V2 that is basically V1 with some add-ons. Also hopes to retire.

Matt (Chair): Some people are passionale about incompatible VN, others care less. Have not heard people say they have issues with the draft as-is. 

Question (chairs):
1. Do people oppose solving both in the current VN draft? (little hands opposed)

Martin Duke: If we ossify on QUICv1 header bytes, we'll need a TLS-style VN mechanism that will look like Compatible. We might as well roll out both mechanisms at once. 

Kazuho: I'm not sure if we are at a point where we can confine to a particular design of compatible version negotiation. For example, we might want to embed the first transcript of V2 in the Transport Parameter that also acts as an indication that v2 is being offered by the client.

Mirja: Don't have a good understanding of what are compatible versions. Designing a mechanism for something we don't undersand is a risk. 

David: Concept of compatible seems well understood (taking packets from one version and massaging into another). 

(Lucas is playing playstation while running the meeting)

Questions (chairs):
1. Do you think compatible VN is a requirement? (count 10/25)
2. Do you think incompatible VN is a requirement? (count 18/25)
3. Do you think compatible VN is a non-requirement? (count 0/25)
4. Do you think incompatible VN is a non-requirement? (count 0/25)

Chairs will confirm this on the list. Editors are happy to take feedback and integrate it into the draft.

TODO(david): file an issue on the draft to add guidance for TP vs VN practices

#### Open Issues
  * See https://github.com/quicwg/version-negotiation/issues

#### Open Floor

### Wrap up (5 min)

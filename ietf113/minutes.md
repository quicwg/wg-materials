# IETF-113 QUIC WG Agenda

* [Meetecho](https://meetings.conf.meetecho.com/ietf113/?group=quic) remote participation
* [Minutes](https://codimd.ietf.org/notes-ietf-113-quic)
* [Meeting chat](xmpp:quic@jabber.ietf.org?join) ([Slack](https://quicdev.slack.com/) users can join the #jabber Slack channel)

## Tuesday, March 22, 2022

09:00-11:00 UTC Tuesday Session I

### Administrivia

5 min total

* Blue sheets
* Scribe selection
* [NOTE WELL](https://www.ietf.org/about/note-well.html)
* [Code of Conduct](https://www.rfc-editor.org/rfc/rfc7154.html)
* Agenda bashing

### Chair Updates

* 5 min - General updates about the WG [slides](https://github.com/quicwg/wg-materials/blob/main/ietf113/chair-slides.pdf)

milestone dating discussion:
- spencer: we shouldn't lie to ourselves. so telling the truth is good, but people will notice if we stop lying. IETF people will adjust, but other SDOs will be startled. please be very clear about what you're doing and why. please drop a liaison note to other SDOs explaining this, especially SDOs that are already communicating with the QUIC working group. without that, having the dates disappear completely might send a message that people should take work in scope for this WG to another SDO, which would be a trainwreck. DTRT.
- david schinazi, quic enthusiast: this is between the chairs and the AD, please just decide.

### WG Items



#### Version Negotiation

* 20 min - Open issues, updates to [version negotiation](https://datatracker.ietf.org/doc/draft-ietf-quic-version-negotiation/). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf113/quic-vn.pdf) - *David Schinazi*

- [issue 90](https://github.com/quicwg/version-negotiation/issues/90), does anyone care?
  - ekr: (no audio)
  - martin thomson: ekr's right, you're wrong. a version is always compatible with yourself.
  - david: proposal: do what ekr wants. everyone OK with that?
  - (silence)

- do we want to tie this to V2?
  - no strong opinions from the chairs.
  - martin duke: I think V2 is waiting for you, so it won't be blocking.

- shall we move to WGLC?
  - mt: having implemented both I think they're technically good. Have implemented V2. They interop. Think we're deploying it. VN draft is a little rough editorially, but will have a look at the new version before agreeing.
  - ekr: if we have substantial editorial changes, let's do them before WGLC.

#### QUIC v2

* 10 min - Open issues, updates to [QUIC v2](https://datatracker.ietf.org/doc/html/draft-ietf-quic-v2). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf113/quic-v2.pdf) - *Martin Duke*

- martin duke: I think this ALPN logic should apply to incompatible versions. Pattern we're developing: if you're doing a new version draft, you should inventory ALPNs and see if they work. Converse is the same -- new ALPNs
- mike bishop: Some protocols might not do the work. Need to write something down about what to do when you're not sure whether the ALPN is compatible with the version.
- md: we've overloaded the word compatible. one, VN. the other, version + ALPN, which is a different question, and that needs to be addressed in new version or new ALPN drafts.
- Mike Bishop: ideally there is a concept of upper-layer feature compatibility.
- david: I don't think there's an ocean of "i don't know whether this works" here. this isn't TAPS, we're not mixing and matching. in hindsight, we messed up alt-svc, using ALPN tokens. what we need is a representation of an entire transport stack.
- md: that's a segue to the next slide... (What about the future?) draft-duke-httpbis-version-alt-svc is the long-term solution to this problem, but it's in front of httpbis.
- david: I personally think we need to solve this. No rush to deploy V2, there's a risk we'll make an even bigger
- mt: anything compatible on a VN and a feature basis is probably OK to use the same ALPN. Need a superset of features. i.e. if you have a new QUIC that's only streams, no datagrams, probably OK for H3 ALPN. Doesn't work if it lose features or compatible version upgrades, due to perf problems. That's what we're talking about in the alt-svc discussion... The chat is balancing toward doing this in VN, not in V2.
- david: QUIC VN draft is (obv) not version-specific, operates at QUIC invariant level. Doesn't involve ALPN, doesn't involve TLS.
- mt: There's a lot of super-invariant stuff in there, though, e.g. retry. This is not a property of V2, but of VN.
- md: V2 specifically will be fine... establishing a pattern. Maybe we can trust future us to revise this pattern if needed. I'm OK putting it in VN though.
- mt: As with alt-svc, we can do the best we can with the information we have -- impl experience suggests we can reuse ALPN within relatively narrow constraints.
- ekr: worrying about this is a bit premature. You won't be ALPN switching between DoQ and H3, for instance. VN is agnostic, but it's hard to believe that other versions won't need something ALPN-like, even without TLS. What has to appear in VN is that any exterior protocol negotiation has to be done from scratch with an incompatible version. V1 -> ALPN A, V2 -> ALPN A | ALPN B. Fallback to V1 must imply ALPN A. There might be other things that have this property, haven't thought about it. But this needs to be explicitly stated.
- md: think we're moving forward with V2 with V1 ALPNs. Maybe hold up VN/V2 for resolution of httpbis draft. Otherwise ready for WGLC.
- ekr: Don't think that's necessary, once the principle is documented in VN.
- md: please wander over to httpbis and express support for this...

#### Load Balancers

* 10 min - Open issues, updates to [QUIC-LB](https://datatracker.ietf.org/doc/draft-ietf-quic-load-balancers). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf113/quic-lb.pdf) - *Martin Duke*

- Martin Duke: One CID format to rule them all; Sec review awaited; split drafts to have retry separate; interop and deployment experience needed
- Ekr: read Ilari's review. Needs more review for the crypto analysis.
- md: there is a zero-pass option, no encryption at all... we could have config to turn the knob on number of passes, need to think about this some more and talk to Christian...
- ekr: ... not sure we should publish something as proposed standard at this level of confidence
- md: have not completely digested this
- Christian Huitema: I have a lot of sympathy for what ekr said, I don't think we should invent stuff. Insisted on crypto review to make sure we weren't doing so. We did get one positive review though. Unclear that the <inaudible> attack is important in our context.

#### Multipath

* 30 min - Open issues, updates to [multipath QUIC](https://datatracker.ietf.org/doc/html/draft-ietf-quic-multipath). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf113/IETF-113%20-%20Multipath%20extension%20for%20QUIC.pdf) - *Mirja Kuehlwind*

- are we sure we really don't need standby? [issue 22](https://github.com/quicwg/multipath/issues/22)
  - spencer: this is really basic, almost everyone who has a mobile that supports Wifi will find this useful sooner or later. could be in a separate extension but then basically everyone in this context will negotiate that extension. not having this in the base will make things harder
  - tommy pauly: you could have implicit ways to tell the server not to use a path yet... but being implicit is complicated. also, very strong argument for having at least parity with MP-TCP.
  - mirja: MP_PRIOR option was originally designed to be more extensible but it collapsed to this functionality.
  - yunfei ma: already see users complaining about cellular data usage; lack of this feature affects user experience.
  - markus amend: fully support this idea. only question: is one bit enough? in MPDCCP we spent four bits (path priority), might consider this as well.
  - mirja: no PR yet, will propose a solution.
  - hang shi: advanced feature with respect to scheduling is not a 0/1 decision, priority should be left out of the base draft.
- should servers be allowed to open new paths? [issue 47](https://github.com/quicwg/multipath/issues/47)
  - mike bishop: issue is not that we want the server to open new paths, but with respect to whether server can send the first packet. I'd see this like an extension to server preferred address. Can't just remove the restriction, you need more machinery.
  - mirja: That'd be an extension we didn't envision. If the server tries to open a path and it doesn't work, then you fail, and you have the
  - marten seeman: having server-initiated path would be symmetric, and useful for peer to peer use cases
  - ekr: p2p you're using ICE anyway...
  - brian: if you release this extension and add text about what you'll actually get, that would be helpful. Very excited about additional cases (e.g. Mike's server preferred address).
  - eric kinnear: I'd be fairly hesitant to release this in the MP extension. Client-initiated migration was chosen to keep us from having to address a lot of fairly painful problems. Might be worth it to keep the restriction in the base case, and relax it in a completely new document (that also spends lots of time on those issues, and adds useful features)
  - mirja: Have forgotten most of that pain, if you have pointers to that please send them along
  - spencer: can this extension draft be silent about this, and have another doc fix this in the base QUIC protocol, is that what eric's suggesting?
  - mirja: just need to dig into the old discussions. hope eric can help with that.
  - Jana Iyengar: removing the restriction doesn't tell us much about the problems that might arise. that probably needs to be in another document...
  - mirja: sounds like people are interested in having that discussion.
  - Christian Huitema: MP option designed to be as compatible as possible with QUIC V1. Departure from client-initiated paths cascades. Who validates? Server can only use it after client validation? Really believe it's better to leave server-initiated for a separate doc.
  - mirja: Disagree a little. We're keeping things minimal, but we make some changes.
  - Christian: Good reason is path validation.
  - mirja: This is just symmetric
  - Christian: No, server MUST NOT send data before client has send validating packets on the path.
  - Harald Alvestrand: Speaking from WebRTC experience, anything that restricts failover is a pain. Server-initiated channels is a useful tool in places other than multipath. Should add server-initiation separately from multipath.
  - mirja: Conclusion: will leave issue open, but reduce priority on fixing it.

- Sending non-probe packets before path validation complete [issue 50](https://github.com/quicwg/multipath/issues/50)
  - yanmei: token mechanisms for endpoints to do quick peer validation. need to consider problems very carefully...
  - brian: note answering this question might make the previous question easier to answer, once we have a faster method for validation that might work symmetrically.
  - eric: why do we need this unless we're sending data on multiple paths within one 0RTT?
  - mirja: AI for yanmei, please add more info to Github issue

- Do we need a transport parameter to negotiate max path idle timeout? [issue 95](https://github.com/quicwg/multipath/issues/95)

  - (no discussion)

- ECN support on single/multiple packet number spaces [issue 87](https://github.com/quicwg/multipath/issues/87)

  - gorry: I don't like the "break ECN" option. Will read and comment.

- packet number spaces [issue 96](https://github.com/quicwg/multipath/issues/96)

  - brian: note that in the multiple PN case you're just instantiating another loss recovery, whereas in the single PN case you have a lot more special-case codepath.
  - martin thomson: there's a code complexity on the multiple PN spaces not captured here, you need multiple key scheduling instantiations as well.
  - christian: point mirja's making here is based on my implementation experience, it's not that big of a mess.
  - christian (slide on PR 103): allow runtime tradeoff between zero-length CID and multiple number spaces. optional complexity, app can choose to use zero-length connection ID and pay with additional complexity in ACK processing.

#### qlog

* 20 min - Open issues, updates to qlog. [Main schema](https://datatracker.ietf.org/doc/html/draft-ietf-quic-qlog-main-schema), [QUIC event schema](https://datatracker.ietf.org/doc/html/draft-ietf-quic-qlog-quic-events), [HTTP/3 and QPACK event schema](https://quicwg.github.io/qlog/#go.draft-ietf-quic-qlog-h3-events.html). [slides](https://github.com/quicwg/wg-materials/blob/main/ietf113/qlog.pdf) - *Robin Marx*

- security and privacy

  - brian trammell: you're right that this is a can of worms. some prior are in IPFIX and PSAMP, let's follow up offline.
  - eric kinnear: per-field indicators are useful. having something in this document that points out places in which information might be exposed, especially in combination with other fields. +1 to follow up offline.
  - jana iyengar: per-field indicator's are very useful, but let's not go too deep down that rabbit hole. value in indicating level of sensitivity, consumers might not understand the risks. you don't have a global view of how the traces are being used, though. these are considerations, not rules. not about getting it perfect.


### Other (aka "As Time Permits")

#### 0-RTT BDP

* 10 mins - 0RTTBDP drafts [draft-kuhn-quic-bdpframe-extension](https://datatracker.ietf.org/doc/draft-kuhn-quic-bdpframe-extension/), [draft-kuhn-quic-careful-resume](https://datatracker.ietf.org/doc/draft-kuhn-quic-careful-resume/) [slides](https://github.com/quicwg/wg-materials/blob/main/ietf113/0rtt-bdp.pdf) - *Nicolas Kuhn, Gorry Fairhurst*


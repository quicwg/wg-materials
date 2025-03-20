## IETF-122 QUIC WG Agenda

## Wednesday, March 19, 2025

13:0-15:00 Wednesday, Session II

notetaker: Brian Trammell

### Introduction / Administrivia

#### Qlog

Lucas: note no agenda time for QLog, only a few issues remaining and many people remote. many of these issues are security-relevant, if you have interest and expertise here please have a look. QLog extensions for specific applications in relevant WGs.

Mirja: fine to do QLog extensions in other working groups. If we want to do this, the WG should make that decision explicitly and write that down in the QLog drafts. 

Lucas: Can leave this to the authors...

Gorry: We should do a turn on the IANA-equiv part of this doc to make it clear how to add an extension. We will want to do last call in QUIC since it owns the core spec, but we need the expertise from other groups.

Mirja: It's straightforward and easy, just need to write it down so we don't have to talk about it again.

### Multipath QUIC update + open issues
-----------------------------------

Yanmei Liu presenting [slides](https://github.com/quicwg/wg-materials/blob/main/ietf122/multipath.pdf)

#### Issue 500

Mirja Kühlewind: do we really need `PATH_CIDS_BLOCKED` or is the case it handles always simply an implementation error? Proposal: we already have the frame, we might not need it but we do understand it.

Mike Bishop (hatless): these frames are more for debugging than anything else. You shouldn't be running into these limits, 

Mirja: `PATH_BLOCKED` is more useful. This one is more often an error on the other side.

Mike: Mainly what I expect an implementation to do is log it. 

Mirja: yep that's valid

Kazuho: +1 useful for debugging.

Mirja: This sounds like close with no action.

#### Conclusion

Mirja: We're done! Next version ready for WGLC.

Gorry (hatless): minrtt. I've sent a few comments. 

Mirja: ...covered in the updates.

Gorry: This might not be just a path property, might also be global. Is it? We need to figure out the scope here.

Mirja: RTT calculation guidance in implementation guidance, not rewritten yet, not super simple, because different implementations handle acks differently, some send the ack on the fastest path. So not 

Gorry: We probably need slightly more text.

Martin Duke: Have quickly read. I like the protocol interop bits. What's the deployment status of this work?

Mirja: Alibaba is actually using this...

Yanmei: For mobile apps talking to our servers, for API request acceleration. Web traffic, not "3GPP stuff"

Mirja: This is also part of the ATSSS spec for 3GPP. This is brand new, will see deployment in a couple years.

Martin: The language about scheduling and shared-bottleneck CC is very carefully crafted not to take research as normative refs, but I'd be really interested to hear about how Alibaba is using this. Because IMO without 3GPP this would be experimental, but maybe I'm wrong, maybe we know more about how all this works. Or maybe we need a here be dragons warning.

Mirja: Github editorial pass makes this better. On Alibaba, a lot of this is for improving handover, this is a bit easier. For ATSSS there is 3GPP guidance here, and there is also a proxy as part of the arch, so obvious bottleneck. For two completely independent paths, this is harder.

Martin: If we just say proposed standard, GA, we are implying confidence we don't have. I don't want people to turn this on and have it work poorly. 

Mirja: If you implement only this spec, you can not just turn it on because you also e.g. need some logic on packet scheduling. This is why we want to get this implemented, to get experience.

Matt Joras: How is this different from MPTCP

Martin: MPTCP is mainly used for handover. We've never standardized a fully multipath transport...

Mirja: (mentions HTTP/1.1 parallel TCP connections)... maybe we should 

Lucas: Could you... (poor single-path network performance) 

Martin: I don't want the general RFC-reading public to think this is ready to use for all use cases, because the general case CC here is open research.

Mirja: In this version, only the client can open paths. So this biases toward the side that has more path information.

Gorry: (5033bis?) says mostly thigs we've said at the mic here...

Lars: I have a client, no plans to implement MP. Don't know whether other major clients plan to ship soon either. Have same concerns as Martin. For most of the other work out of QUIC WG we've had more interop before publishing. 

Mirja: We have six implementations

Matt Joras: I don't think you should downplay the Alibaba one

Lars: Don't see a lot of support otherwise. I don't want to make this experimental, but I want to make it even more clear that this is a set of building blocks for making MP, not a full general purpose solution. cf. Costin Raiciu talk in ICCRG, talking about how this works in DCs, where the approach is different, uses packet spraying. This seems like a more modern way to do MP, so I'm not sure why we're still working on heavyweight per-path approaches.

Mirja: We're done with the foundation now, so now we can go work on that.

(Lars and Mirja argue for a bit)

Christian: We have a clear use case for better failover. There are use cases for P2P establishment (proxy to direct handover, ICE replacement), MP makes this *way* better. We have a lot of experimentation going on. I get weekly queries from researchers looking to use this.

Brian Trammell: DMTP in PANRG. Useful to publish this as a PS with caveats, because this is a foundation not just for production deployments but also current research that will lead to future production deployments.

### Address Discovery update + open issues 

Marten Seeman presenting [slides](https://github.com/quicwg/wg-materials/blob/main/ietf122/address-discovery.pdf)

#### Issue 41

Kazuho Oku: Prefer status quo, as we have the option to avoid collecting information from clients, which is always a privacy concern that has to be taken into consideration.

(call for Martin Thomson, who is not present)

Marten: my understanding that this is ok for operators...

Mirja: I removed the word "negotiation" from the MP draft because it's an announcement, take it or leave it.

Marten: good point


### Receive timestamps 

[draft-smith-quic-receive-ts](https://datatracker.ietf.org/doc/draft-smith-quic-receive-ts/)

Joseph Beshay presenting.

Lars: I think there's interest, punted in V1 work. Would love to hear more about what CC is doing with the information. We had a version of the ACK/ECN frame discussion earlier when we decided not to make this extensible. This is a different design but not sure it works. need a version negotiation or a length field in the frame. I support the ack-extended frame, need to know how much to skip if I don't know the bits yet.

Joseph: That's part of the negotiation... If we don't think we're going to add more to the ack in the future, this is overly complicated.

Martin Duke: We have lots of frame types. Just use more.

Joseph: if we end up with more optional fields later, we get exponential growth

Martin Duke: Yes, 2^n extensions, but N is small

Christian: What about multipath? It defines its own ACK extension format, because different paths have different sequence numbers. We already have a version of the combinatorial problem. We either need a composable solution, you send a side frame with additional information. Or we need an ack format negotiation. 

Ian Swett, MoQ hat: demand for this will increase, MoQ will use a variation of GCC or Screen, almost all of them require some flavor of this. QUIC hat: thanks Christian for bringing up multipath, this leans me toward #4 fairly strongly. 

Jonathan Lennox: ... (implementation detail discussion with Ian and Christian)

#### Poll

Should the QUIC working group adopt a draft working on ACKs with receive timestamps? 30 yes, 0 no, 8 no opinion. 

### Extended key update

[draft-rosomakho-quic-extended-key-update](https://datatracker.ietf.org/doc/draft-rosomakho-quic-extended-key-update/)
------------------------------------------

Yaroslav Rosomakho presenting

David Schinazi, clarifyin on slide 3: what do you mean by compromise, memory on the device, stream cipher compromise...?

Yaroslav: both. anything that gives you key material.

Lars: TLS has a broader applicability than QUIC, so maybe look at a way to do something simple just for QUIC

Yaroslav: yep, we can look at a more restrictive design here.

(on questions slide)

Christian: I have a couple of issues here. One, this design forces us to keep the TLS context for the full connection duration. That's a tradeoff. If I destroy the context as soon as negotiation is complete, I don't risk having the memory stolen.

Yaroslav: You need to keep the context for a couple of other reasons? Oh, not allowed in QUIC.

Christian: I have practical experience in long-live sessions in QUIC, and my current advice is "don't do that". Because of UDP, you have to send a lot of ancillary traffic to keep NAT state. If you have a long application session, we recommend session resumption over multiple QUIC connections. We have to have some discussion in the WG about what the best way to do long-

Matt: let's talk about the applicability of the problem here

Martin Duke: We should try to support all the TLS1.3 features that are relevant, this doesn't seem like a huge implementation lift, let's keep the CRYPTO stream open for TLS machinery that is already there. Christian's point about state leaking, we should think about that. 

Yaroslav: If we had an alternative design that didn't rely on the CRYPTO stream, would that be better?

Martin Duke: CRYPTO stream is less software effort. Not being able to reuse TLS code here is scary for obvious reasons. If it's just different wrapping, that's better.

Varokas: How do I know the key is compromised, or do I just assume it has been?

Yaroslav: This just happens periodically based on timer or byte count. It's blast reduction. 

John Mattsson: Very relevant. Typically we do this hourly for SSH. Christian prefers resumption, but this is more complex. I think we should do this, esp. for 3GPP infra.

David Schinazi, QUIC Enthusiast: QUIC was designed for short sessions, because any protocol that is client initiated fits that patternw well. For MASQUE this is less possible. Would be good. Resumption requires previous app secrets. In practice, what everyone does is keep TLS. Do not invent something other than the CRYPTO stream. The min duration between key updates needs to be a transport parameter. I think you can resolve all these problems, we should adopt.

Magnus: also support. Another long session aspect we need to discuss, related to mutual reauth. Not included in this draft?

Yaroslav: We want reauth to be separate, they solve two different issues. Reauth is good, not this draft.

#### Poll

Matt: we should talk about long-lived sessions in general, lots of good commentary there, but this is a specific question about this draft:

Should the working group adopt work tackling extended key updates in QUIC? 26/2/11, 123 in the room.

Lucas: of course we take the discussion to the list

### Source buffer management

[draft-cheshire-sbm](https://datatracker.ietf.org/doc/draft-cheshire-sbm/)

Stuart Cheshire presenting:

question from Stuart: is source buffer management applicable to QUIC?

Ian: our implementation is pretty good about queueing in the QUIC layer, but some devices have terrible queueing downstream. My code is OK. But that might not be enough.

Stuart: Please share the information about how you solve this. If you haven't thought about this, you probably have a problem.


### Qmux (formerly QUIC on streams)

[draft-kazuho-quic-quic-on-streams](https://datatracker.ietf.org/doc/draft-kazuho-quic-quic-on-streams/)

QMux. Alan Frindell presenting. 

Gorry, hatless: this work has an implicit message that QUIC and TCP have long-lived futures. we should 

Alan: Do we believe that reliable bidirectional sockets have a long-term future? Domain sockets and RDMA have the same shape.

David Schinazi: thanks for splitting this off the HTTP stuff on top. Wish we had done this back in RFC 9000. H3/H4 over this, I have concerns. This piece is useful. QUISPATCH? I think we should send this not-to-QUIC. Renaming it away from QUIC helps. Putting it in the QUIC WG goes in the other direction. TSVWG? 

Eric Kinnear: Thanks for this. Audiences matter a lot, there are at least four distinct audiences. Not as worried about H3, since this is basically H3/QMux/TCP as compatibility mode. This is a good thing to do. I don't mind doing this here, the right expertise is in the room.

Ian Swett: As a QUIC editor, I am very glad we did not do this then. Wish we'd done it the next day though. Late is better than never. As an MoQ enthusiast, that's not entirely accurate. Branding and nomenclature will be very hard to get right. QUIC: It's the right people, you can make them meet in another room.

Kazuho: This is why we designed H3 and QUIC as distinct protocols. We should do this. I think we can do this in QUIC. People outside the IETF don't care about the distinction

Lucas hatless: I have people who really want this thing. The thing they want is the similarity to the QUIC stream model. The wire encoding is nice to have, but compatibility in the shape of multistreaming in parallel is very powerful for building scalable deployments. If we don't do this in QUIC we would end up with a design space explosion that ends up in a fizzled effort, which I don't want.

Yaroslav: I want a single API here, so I strongly support this work. Reusing the QUIC bells and whistles on TCP might not be the most efficient way to do this

Lars Eggert: We should manage external comms separately. I like Eric's suggestion to name it to imply degraded functionality WRT QUIC. I think we should do it in this group. 

Cullen: Simple comment, obvious name for it is SLOW. The important thing is that it requires us to document the API. The API of SLOW and QUIC can therefore not diverge

Brian Trammell: what Cullen said. Tired of teaching QUIC and explaining to students that we don't have an API. We understand how to spec the API now.

Alan: go look at WebTransport

Zahed: Messaging. Don't kill QUIC as a generic transport protocol. 

Matt: This will require a recharter, according to chair and incoming and outgoing AD opinion. Will follow up on the list WRT that.

Round of applause for our outgoing AD.


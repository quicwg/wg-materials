# IETF-115 QUIC WG Agenda

* [Agenda](https://github.com/quicwg/wg-materials/blob/main/ietf115/agenda.md)
* [Meetecho](https://meetings.conf.meetecho.com/ietf115/?group=quic) remote participation
* [Minutes](https://codimd.ietf.org/notes-ietf-115-quic)
* [Meeting chat](xmpp:quic@jabber.ietf.org?join) ([Slack](https://quicdev.slack.com/) users can join the #jabber-zulip Slack channel)


## Monday, November 7, 2022
13:00-15:00 Monday, Session II

### Administrivia
* Blue sheets
* Scribe selection
* NOTE WELL
* Code of Conduct
* Chair Updates

## Agenda bashing
Martin Duke: Please attend the congestion control working group side meeting, Thursday at 5pm

## General updates about the WG
QUIC Retry Offload is going into the deep freeze until there is implementer interest.

## Open issues, updates to multipath QUIC - Quentin De Coninck
See slides
Yunfei Ma: Does anyone have a solution for better RTT measurements with single packet number space?

Martin Duke: Didn't we get rid of single packet number space last time?

Quentin: 0-length connection IDs mean that you're still in single PNS, which makes things a lot more complicated. We'll discuss later if we want to keep this at all.

Martin: I thought we'd gotten rid of it entirely last time, but thanks.

Ian Swett: Should we ditch single packet number space -- let's just talk about that now.

Quentin: Is there a use case that needs zero-length CIDs (and therefore single PN space)

Kazuho Oku: Could be a privacy problem (given original prohibition against ZLCIDs (zero length CIDs) for address migration)

Mirja Kühlewind: RFC9000 allows ZLCID with migration!

Eric Kinnear: Does any QUIC implementation really need ZLCID? If not, kill it (silence, head shakes no)

Mirja: If MP is requested when there is no CID, you MUST NOT do it?

Alessandro: I don't think we will support ZLCID at all. Most probably won't, so they ought to speak up now.

Matt Joras: Shall we do a poll?

Alex Chernyaovsky: Why not bind multiple connections together using connection ID mappings instead of doing multipath?

Eric: Splitting streams across multiple paths is valuable

Alex: Yes. Should the abstraction be inside the QUIC connection?

Ian: Requires really clean split between connection and session layer -- doable but takes a lot of analysis. Ought to be a draft.

Lucas: Always willing to look at new proposals, but we adopted this already. Adding a third option is negative progress.

Ian: Definitely kill single PN space

Tommy Pauly: Agree with everyone, kill single PN space. If Ian wants to do a QUIC connection binding, that's orthogonal to this. But we want MP-QUIC.

Christian Huitema: Sure, some scenarios are supportable with binding, but that's much of the same complexity plus multiple handshakes. Also, let's kill single PNS. Keep it simple.

Ted Hardie: MoQ enthusiast. Streams on multiple paths is very important, keep MP-QUIC. MoQ will go there.

Yunfei: We considered connection binding; not just bandwidth aggregation, but also scheduling at the packet level. Alibaba will not use single PN space.

Mirja: Want to verify that the server will not negotiate MP support if there is no connection ID.

Question: SHOULD WE REMOVE 0-LEN CIDS/SPNS FROM THE CURRENT DOCUMENT?
[Poll is 53-2 (out of 165) in favor of discarding single PN space ]
Lucas: we'll take it to the list to confirm consensus.

Mirja: Any no votes want to speak up? If not, they can reach out to chairs.

[talking about keepalives, slide 4]
Eric: Should we make it clear that there is a multiplicity of paths to keepalive? Is it an interface problem to specify what paths matter?

Mirja: interface could punt the decision to the application, but maybe not

Eric: We could just do an extension for this later. Don't need to hold things up

Jana Iyengar: This is tied to scheduling -- it's an application question. Very context specific.

Mirja: If you ping only one path and it fails, you have to kill the connection

Jana: OK

Matt: Please add this stuff to the issues

Lars: QUIC is great because keepalives matter less with 0-RTT. So no big deal if paths or connections die.

Jana: +1 to Lars. Is there a latency penalty for a new path

Quentin: Path validation

Jana: unnecessary to restore a path

Christian: +1 to Jana.

Mirja: To clarify: we are not saying you can reopen a path without validation.

Yunfei: there is a penalty for not keeping the path alive. Congestion window will be reset.

Jana: RFC9000 already allows storing path state.

Eric: Let's move along

Matt: Take it to the list or github

Mirja: We always require path validation in this draft because it's different

Eric: Let's take it offline -- There's a bunch of machinery around migration that was designed to take care of a bunch of these concerns, we should make sure we still allow that and probably use it to our advantage here, as well.

Jana: I'm happy to discuss offline, but it should be the same as RFC 9000.

Eric: (Thumbs up)

[PATH_ABANDON(slide 6) crosses paths with RETIRE_CID]
Mirja: Why change path ID when connection ID is changed?

Christian: Why not just resend? If you see that the CID has changed but you keep getting in data because the peer has not abandoned the path, you either send it again or you close the connection. Should be simple, nothing super complex here.

Martin Thomson: I've always been a little bit uncertain about using CID sequence number to identify paths. If either endpoint changes CID, you are now swapping sequence number. Mirja is probably right here, we probably need the additional level of indirection. When you say that I'm abandoning my path n, you might have path m which is the same path, and the other side has p and q which are the other end of the same path.

Christian: Let's remember why we used CID seq number as path ID. We want AEAD, AEAD needs a nonce, the nonce is the sequence number. If we do that, we need to make sure that the same sequence number and the same path ID never happen at the same time. This means that the receiver needs to have the path ID inside the encryption. Receiver only sees the connection ID. Receiver needs immediate link for CID in encryption context. If you break that linkage, then you have relation with encryption.

Eric: What if you want a different CID for every packet, that's very heavyweight

Martin: Something's confusing here. Are paths unidirectional?

Quentin: Yes, CIDs are unidirectional, path abandon kills both sides

Martin: Why not use CID controlled by host A and then you don't have this issue

Ian: I was going to suggest something different -- just use the ID that initiated the path, that would be stable over the lifetime of the connection. That or Martin's suggestion would work.


## Open issues, updates to Acknowledgement frequency - Ian Swett
see slides - hot off the presses

Ian: two things happened
1. removed ignore-ce because it might be dangerous and value is low
2. PR to change ignore-reordering to reordering-threshold; need to update based on feedback. Please take a look.
In good shape other than editorial issues

Matt: Shouldn't reordering threshold be a varint?

[The room wants a varint]
Gorry: How big can it be?

Ian: 2^62-1

Gorry: sounds big compared to other RFCs

Ian: We could add some text but reluctant to have a hard limit

Gorry: You are redesigning transport considerations here, but big is too big

Matt: Varint question is different from limits

Ian: if threshold > cwnd, it doesn't matter anymore because other mechanisms kick in

Jana: (1) We don't know what is large (high BDP paths) (2) varints make life easy -- don't have to change wire image ever again. (3) We don't know the right number so leave it open to experiments.

Ian: I used UINT8 because that's what Linux TCP does.

Jana: Linux implementation, not the standard

Mirja: RACK says 1 RTT, so that's not a hard number.

Gorry: How close to being done?

Ian: This is it, the rest is editorial

Jana: WGLC in the next month

## Open issues, updates to qlog - Robin Marx
see slides

Mirja: DATAGRAM is not part of this currently?

Robin: all non-core RFCs will be their own document

Mirja: That's a silly number of little docs

Lucas: The backlog continues while lots of extensions keep appearing -- want to finish someday

Mirja: Don't need to be religious about it. DATAGRAM is really popular.

Quentin: Does QLOG indicate Connection ID used in a packet.

Robin: Yes, if you log the packet header

Quentin: Maybe the path ID could go in there.

Robin: in the base drafts?

Quentin: have to know IP/port change for migration

Jonathan Lennox: Should cover everything up to pub, then put it on the other draft.

Martin Duke: Let's not try to capture everything, let's get things published and we can then extend later as needed.

David Schinazi: RFCs are expensive. Just have a cutoff, then decide as needed.

Christian: Publish the draft now

Mirja: We could definitely use this for MP.

## Open issues, updates to QUIC-LB - Martin Duke

Martin: Last time we met, we decided to sit on it until deployment happened. Should be deployed by Yokohama or at least San Francisco. Anything the group wants to hear in a report, other than we did it and it works?

Matt: As far as we know, we haven't seen a lot of interest in deploying it yet, so we just want someone else to do it.

Ian: Might be worth mentioning the silo issue

Martin: There's a non-normative section around multithreading and problems, most of us have multithreaded servers.
Can treat it like a L4 load balancer. Have it decrypt the CID and then define which thread should get it.
Envoy uses BPF and you're not going to be doing the crypto in BPF. Alternatives:
1. Thread can register with the demultiplexer and just have a big table.
2. Can make a bitmask that applies to non-ciphertext part of the connection ID

Doesn't need to be standardized, but it's nice to have some text to make things clear and give people good ideas.


## Reliable QUIC Stream Resets draft-seemann-quic-reliable-stream-reset - Marten Seemann
see slides

Matt: As an stream implementer, I'd rather not mess with it anymore. What if we put some additional application data in the RESET_STREAM instead? No change to state machine!

Jana: Current semantics are clear; this muddies it. Value seems small. Could just FIN!

Marten: Happy to hear other solutions because I am definitely running into this problem, and solving at application is wrong. FIN doesn't really work with application semantics or if there is a lot of data that is not reliable.

Jana: This is a stream mapping problem. I don't want to design on the fly.

Lucas: H3 has these problems already. It's surviving but not airtight

Mike Bishop: H/3 had a late add on unidirectional streams -- do
not reset as receiver before you know the push ID. This solves the same problem by the send side. We can live with it by leaking identifiers, but not optimal. I support this work.

David Schinazi: I have not seen this problem in practice. Just don't reset all the time! In WebTransport, using a capsule is much simpler. Matt's proposal to append stream data in the frame is acceptable.

Lucas: Does that feel in scope for QUICWG? [No objection]

Marten: WebTransport solution has bad corner cases. Will discuss in that WG.

David: WebTransport will decide if they need help from QUICWG.

## QUIC FEC draft-michel-quic-fec - François Michel

François: See slides

David: Were the losses induced or natural?

Francois: Natural

Spencer: FEC was in the original charter but abandoned. I'm glad to see this resurface.

Jana: The FEC frame is during idle time?

Francois: When there is no user data to send

Jana: You could try sending some proactive retransmissions. Fastly already has that.

Christian: Great idea. Tried repeating last window of packets. It helps! Would like to see statistics of loss patterns on these
links.

Yunfei: We are interested in the loss interval too. Bursty or not? Link layer often has FEC to fix isolated losses, so you just have bursts, where FEC doesn't work so well.

Martin Thomson: Why protect frames? Application data is most important. Frames are not always the same across retransmissions.

Francois: Control frames or DATAGRAM.

MT: Controls have their own retrans mechanisms; DATAGRAM is lossy

Gorry: Very little about congestion control here. Are you going there?
[Question going offline, out of time]
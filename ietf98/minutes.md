# QUIC WG Meeting Minutes: IETF 98


## Administrivia

Chairs presented note well.

Note taker: Magnus Westerlund

Chairs reviewed the proposed agenda. No changes.

Noting the seating layout experiment and how that will work. Request for feedback on the experiment.


## Chairs' Overview

There are number of outstanding consensus call on issues, they will be open another week.

If you haven't please review and provide any input.

A badge has been designed that can be used to identify the effort.

Aiming for first implementation draft after Paris interim. Focus and identify issues that gets to
being possible to implement. Jana Iyengar asked how those will be determined. Proposal for using a
special tag "Blocks Implementation" in GitHub.


##QUIC Applicability and Manageability Statement

Proposals to consider for adoption:

* Applicability of the QUIC Transport Protocol
* Manageability of the QUIC Transport Protocol

Presentation by Mirja Kuehlewind.

Mirja noted that the applicability statement will be wider than H2.

Question around transport interface.

Martin noted that this can be a significant effort, and may be to early as we expect a lot of
changes in the future. But, it would be interesting nevertheless.

DKG: API is a critical piece.

Eric Rescorla (EKR): no one arguing it is not useful.

An API specification would be a separate document.

Gorry Fairhurst: the API should be a separate document, as it is easy to update.

Manageability

Sean Turner, noted it was clear that it is work in progress.

Chairs asking about adopting these documents as WG items.

20-30 people had read them. Strong consensus for adopting, with no one opposing.

## Working Group Drafts

### Transport (presentation)

Jana presenting.

Ted Hardie: there are potential privacy issue here. Talked about changing the connection ID on reconnect.

Jana: clarified that once the server has set the final ID, then you don't use the old. Ted, can you force a client back to the original ID?

Mike Bishop: talked about it, considering a frame type to request a new connection ID.

EKR: don't get to attached to the design. Considering more radical design. What is the threat model? Stopping

Victor Vasiliev: can we ship multiple connection IDs and how can you do that?

DKG: agree with EKR, there is no way a client can prevent a server from de-anonymize them. EKR agree, that the design would require effort to reveal client.

Q (unknown): Why does the client have to send an initial connection ID in the first place?  If we cannot use it subsequently for routing.

Martin T: the design is so that the client immediately pick a new Connection ID. Jana, as the server can choose to use the client's one. And the change can be done at the last hand shake phase, when it avoids any issue.

Jim Roskind: this you need be careful. This is the most ossifying part. For rebinding, a connection ID will be crucial importance.

Hannes Tschofenig: Some of this was discussed in the TLS meeting.

Martin: The issue Jim raised, is that 64-bit is not sufficient for some of the many purposes it is being used. While it also uses a lot of bytes in the packets.  We are sticking to 64 bits for now, until we have a better grasp on the problem.

Jana: in the common case when you are not including more than 2-3 bytes of header.

Todd Short: HW implementation want nicer formats.

Martin: This doesn't seem to be a showstopper for hardware. Unless we have good use for the bytes, we should not send them, even this makes less nice formats.

Praveen: the type field doesn't have any reserved bits for future use

Jana: there a many packet types unused so that one could design something with.

UDP checksum, is not being discussed in the transport.

Igor Lubashev: we considered putting in hashes as protection.

Mirja: what are the assumption on the connection ID setting in the short header? Does it make sense to set it on every packet.

Jana: in the bandwidth sensitive way we don't include connection ID, and the clients always send conn_ids in every packets.

Jonathan Looney: consider h/w implementations for header design.

Jana: looking for people to provide feedback on this.

EKR: I don't understand why it would be useful in every packet. Having it in a single location is not helping, it only ossify it worse.

Robby Simpson: Long header, is there a reason why it is last, rather than first.

Mirja: the connection ID is always in the same place when it is present.

Robby: if we change the packet number for example, then it would be moved.

Mirja: if you have a new packet type, do you have to change version or can you figure it out some other way. Jana, that is not well defined yet.

Martin continuing from Versioning slide.

Victor: can the client choose to use the default? If not do they indicate what they are using. Martin, no, they are not indicating, which Martin don't like.
Magnus: there is too little text on MTU to be implementable.

### TLS (presentation)

Sean Turner presenting.

Mirja: the transport parameters, is this something that needs to go to into the applicability stament.

Jana: no. Mirja, do we need to talk about those transport parameters? If someone invents a new.

MNOT: Sounds like a seperate document. Mike Bishop, there need to a be list of stating what parameters need to be handled by any replacement to the TLS handshake.

Kyle Nekritz: if the header is unencrypted does that mean it is not protected? EKR, it is protected by the TLS layer encryption for handshake.


### Recovery (presentation)

Presented by Ian Swett

Take a look at the editor copy from the git repo and provide feedback.

EKR: Do a -03 version to avoid too much divergence

mnot: Helps to keep all drafts in lockstep version numbers

Martin: All should be providing a new update shortly after the meeting.

?: Is it an explicit goal to track the Linux kernel doing. They have removed some features.

Lars: Free to use standardized congestion control.

Ian: Want to use New Reno equivalent

Jana: seperate loss detection from congestion control. The mechanism are different.

?: Linux kernel sees a lot of churn. Are we going to track that?

Yoshi ?: Timed-based vs. ack-based cc.  We should choose what to use.

Google currently implements both.  Could even be mixed.  Need to provide some guidance.

Lucas Clemente: quic-go currently has a wip-PR for it, will probably be merged next week


### HTTP (presentation)

Mike Bishop presenting

... including the issues they attempt to address. The editors will give presentations summarising their current state.

## Open Issues

### 167 - Hash for unencrypted packets

Martin: Looking for something better than TCP Checksum.  Want to have this resolved.

Jana: Google picked right now FNV-1a.  Because it was simple to implement and does the job.

EKR: From my perspective, use something that we already have. Like AES-GCM.

Victor Vasiliev: Do you suggest that we analyze the different pro and cons.

Jana: it is for the unencrypted packets in the beginning.
AES-GCM regular (No adreversial issue)

Victor: It do goes with profile so it is not unimportant.

Martin duke: AES-GCM, we only only use the same code path, only changing the key when it has agreed. Using the non AEAD Additional data. Have no preferential.

Mike: Using AES-GCM looks good, as it makes the packets look the same.

Jana: prefers something fixed for all time.

DKG: Using AES-GCM makes it stick and can't be ripped out when it obsolete for crypto, but not for hashing.

Erik: Using crypto functions to not provide crypto properties might be misleading.

?: Is there a seperate consideration for middleboxes.

Lucas:  with option 3 a client cannot choose to only support chacha, but always has to implement aes.

Jana: it is not clear what the individual benefits are.  Makes is hard to reason about.

Hum, three ways (Multiple hums allowed):

* CRC-32: some hum
* FNV-1a: strongest hum, clearly
* AES-GCM fixed keys: Almost none

FNV-1a: clear consensus


### 45 - Handshake protocol selection

Proposed resolution: The version number implies a crypto handshaking.

Subodh: handshake indication is later verified in the crypto handshake. If there are multiple protocols, then a man in the middle can influence selection to the weaker.

EKR: you can only avoid this if you don't have crypt protocol negotiation at all
From QUIC point of view TLS should be considered as one protocol as it has its internal version negotiation.

Ben Kaduk: If your security is tied to the weakest, do we expect to see other versions not coming from the WG?

Martin: yes appear to be desired, but it has downsides. The issue can be fixed for HTTP, by specifying that HTTP MUST use TLS.

EKR: There are three alternatives. 1) Version indicates crypto. 2) No wire indication, based on intended context. 3) Wire indication. 1 and 3 both have down-grade possibilities (they re practically identical from a security perspective).

Ted Hardie: There are three linkaging and they need to be kept to ensure the whole chain is secure.

Mike Bishop: the application can already state what version (and thus crypto) it needs.

Jim Roskind: From application protocol, TLS, QUIC. ?

Jana: having HTTP require TLS looks reasonable.

Mirja: if one want to use pre-shared keys. EKR, still use TLS.
If one have to rev the protocol then one do get a combinatorial explosion.

Ted: So it is the different handshaking protocols that matters. Different ciphers are negotiated inside TLS.

DKG: We are saying that the version for the initial version of QUIC is TLS 1.3 or higher.

Ben Kaduk: We do not get new TLS versions that offen. We can consider to have strict binding to a specific TLS version.

Martin: or higher version are likely fine.

Mike Bishop: this is an issue that is already fixed. TLS handshake includes offered versions.

EKR: Clarifying that for any QUIC version, the minimal version of the handshake protocol is required. The application can then specify the requirement. This can be a set of allowable QUIC versions.

Jana: What is the application mapping?

Martin: The application can state QUIC version X and this would be mapped to the implied handshake version (e.g., TLS 1.3).

?: The QUIC version should define the transport. The application should state which security protocol to use.

No consensus.


### 61 - Silent close

EKR: IF one develops a new QUIC application. SSH over QUIC, what do happens if one send a close. Then it is up to both sides SSH application to close down each side connections. No indication of graceful close and ensure that signal has made it. Should not move to a model where one silently closes leaving state in cases one.

Stuart Cheshire: What is in charter, to figure out what information QUIC indicates to middlebox. If one does not provide an explicit signal then, the scavenger timers in the middlebox will be very short, and not allow long lived flows.

Martin Duke: numerous issues on Github about connection close.  One option mentioned: always send a public reset. It's another packet but could help.

Jana: this can be figured out. Stuart's point is well taken. But how important is this really?

IAN Sweet: We are conflating two issues. The question if one sends a packet to close the connection. Or if the application tells the transport to close it down.

Igor Gashinskiy: echoes that Stuart says. Need to have signalling to middleboxes. Sees major risk if QUIC dominates the traffic in a couple of years.

Philham Baker: I agree with Stuart. Do you want to have an explicit role from the middlebox, telling the client, do you want to keep this around? Need for document that tells how Middleboxes should treat flows? How do one handle really long lived flows, longer than current TCP connection time out.

DKG: Question for load balancer, they are in working together with either end-point. We are talking about connection close. We have the option to have a close that is only visible to the endpoint.

Martin Duke: middlebox visibility issues closely coupled to the application layer signalling issue. Need to ensure visibility to the middleboxes. Must be public reset then

Stuart: There has been good discussion. Elaborate. If one view the world as all communication is initiated by the client, then there are no issues. The problem is where is when it comes from server to the client. Like an IMAP server, keeping a connection to be notified when an email happens.

DKG: This is a problem anyway. We need to handle the case.

Stuart: Doesn't change problem. But changes the common case vs. the corner case.

Gorry Fairhurst: +1 stuart. Lets not force timeout, when we can signal explicit.

Jim Roskind: In some applications one do care about not having to wake up. We need to factor all the cases in.

Ben Schwartz: Anything that assumes that QUIC is not deployed is false. We can't assume change of middleboxes.
Privacy leak when connections revel their lifetime.

Martin: people are unhappy that silent close exists.


### 391 - Packet number echo with variable-length numbering

Jana: The usefulness for this is not only endpoint RTT. A AQM in the network can use this to measure.

Jörg Ott: The other ACK packets, do have latency since received. Do you need more information.

Mirja: Minimal should be enough.

Lars: How often should it be included.

Mirja: Once per RTT, or always

EKR: If we need RTT estimation, then a estimation field should be included. Don't have backscatter.

Ted: If one like include this, include an explicit RTT to avoid backscatter.

Ian: If one are in the middle. the RTT downlink may be most relevant.

Ted: Some want to include

Mirja: Are there privacy issues with the additional echo field (in addition to the privacy issue the packet number already has)?

Ted and ?: Yes!

Jana: This shows the importance of the discussion. Use case is real.

Marcus Ihlar: issues with rolling out buffer management. Need RTT from point of AQM. Not only end-to-end RTT.

Ben: Run STUN or other protocol to decouple this from QUIC.

Xavier Marjoij: Need collaboration with the network to ensure that QUIC remains quick.

Eric: having this available as an optional thing may make the network operation saner. Then it may be a good idea, but needs to be optional.

Jim Roskind: One of the vague regrets. Can't do TCP termination, mid stream, which makes me sad. But, at the same time leakage also makes me scared. This is a slippery slope channel. Go for explicit middlebox to protocol interactions, trust and verify.

?: We have been doing rtt measurements for tcp for years, just for network measurements. Risk of losing visibility for network management.

Jana: Need to seperate issues out. ECN needs AQM, to do AQM efficiently we need information.

Marcus: Middlebox vendors will always try to analyze information. Being clear on what explicit information is provided.

DKG: fear about privacy leak is coming from folks not necessarily sure what the true privacy implications are. Shouldn't dismiss this. Appreciated.

Chairs: Take this to the interim if there is sufficient interest and the right mix of people participating. So please talk to chairs if you like to have the discussion.



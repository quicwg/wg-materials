# IETF-117 QUIC WG Agenda

* [Agenda](https://github.com/quicwg/wg-materials/blob/main/ietf117/agenda.md)
* [Meetecho](https://meetings.conf.meetecho.com/ietf117/?group=quic) remote participation
* [Minutes](https://codimd.ietf.org/notes-ietf-117-quic)
* [Meeting chat](https://zulip.ietf.org/#narrow/stream/quic)

## Tuesday, July 25, 2023

09:30-11:30 Tuesday, Session I

### Administrivia

* Blue sheets
* Scribe selection
    * notes: Watson Ladd, Robin Marx
* [NOTE WELL](https://www.ietf.org/about/note-well.html)
* [Code of Conduct](https://www.rfc-editor.org/rfc/rfc7154.html)
* Agenda bashing (unbashed)

### Chair Updates

* 5 min - General updates about the WG [slides](https://github.com/quicwg/wg-materials/blob/main/ietf117/chairs.pdf)
    * Compatible version negotiation RFC 9368
    * QUIC v2 RFC 9363(check with materials, notetaker wasn't fast enough)

### Multipath

* 30 min - Open issues, updates to [multipath QUIC](https://datatracker.ietf.org/doc/html/draft-ietf-quic-multipath).
* [Slides](https://github.com/quicwg/wg-materials/blob/main/ietf117/multipath.pdf)
* presented by Yanmei Liu & Quentin de Coninck

**Yanmei**:
* Diff
    * New transport parameter, no longer remembered
    * Frame types updated
    * Error codes updated
    * CID usage changed
    * RTT guidance added
    * Editorial clarifications
    * Key update mechanism changed to use 3x max PTO
        * Difference from v1 that used one active path
* Interop reports
    * already 5 implementations that support multipath
    * Interop tested 5 ways: not quite there but in progress
* Open Issues
    * PATH_STATUS
        * Two values, what about others?
        * Share sequences across frame types?
        * Or define unknown value behavior
        * **Kazuho Oku**: bikeshed about how to send the same shape. No new info since previous meeting. Prefer different frames
        * **Mirja Kuehlewind**: prefer first solution. As Kazuho pointed out, not the first time.
        * **Christian Huitema**: Multiple easier for IANA issues. Have to maintain sequence only problem
        * **Alessandro Ghedini**: 2 better, easier to add more so won't need to change the PATH_STATUS frame (?)
    * Error codes
        * Only one now
        * Need more
        * **Alessandro Ghedini** : Error code useful for interop but can just use reason field. Don't think we need more
        * **Mirha Kuehlewind**: Think we only use this once, more generic errors used for other reasons. Point of issue was more holistic examination.
        * **Christian Huitema**: If we have multiple only in debug? Rely on reason can switch more easily for debug. Implications on security revealing internal state
        * **Martin Thomson**: Had conversation on weekend, probably worth spreading more widely. This error code from one side trying but hadn't sent parameter, but other peer hasn't. Can still send errors even when peer doesn't support.
    * Packets on unvalidated
        * How to acknowledge?
        * ACK_MP on different, is nonprobing
        * Should it be probing?
        * **Kazuho Oku**: Remove probing frame from multipath concept.
        * **Yunfei Ma**: Multipath for redundancy, if ACK_MP on other path, redundancy broken
        * **Christiain Huitema**: We have other ways to validate paths via PATH_STATUS
        * **Eric Kinnear**: Probing frame is about saying you can keep up
    * Handling packet with new CID and 4 tuple
        * Path validation currently needed
        * Options: guess, bundle RETIRE frame, bundle PATH_abandon, new CID abandon
        * **Marten Seemann**: relevant to next
    * Separate PATH from CONNECTIONS
        * CID = QUIC path with packets numbers
        * Simultaneous use up to active_connection_id_limit paths
        * All paths share same common key
        * Gaps in sequence
        * Abandon by sending frame with the CID
        * Alternative: preassign path ids and CIDS
        * Set that share packet number space
        * Paths can use different keys
        * **Kazuho Oku**: Very disruptive change
        * **Marten Seemann**: Server sees new four tuple, NAT rebinding, must probe. Terminology confusion. Path vs. 4 tuple. No new controller, but but will need to probe tuple. Upside: clear this wasn't intentional
        * **Yunfei Ma**: We also had this discussion a long time ago. Different to preassign. If connection 1 week, don't know paths used. NAT rebinding ping frames not frequent. Should measure.
        * **Christian Huitema**: doesn't like it, many things combined. Encryption vs. paths. Multiple contexts drives up memory of idle connections. Limiting paths runs into temporary paths during rebinding. Can split these decisions.
        * **Mirja Kuehlewind**: Knowledge of paths is not baked in. Fails in NAT rebinding and new CID, after idle timeout. Not common, congestion control ran out. Problem don't know what path to use, close old as quickly as possible.
        * **Martin Thomson**: Join crowd against, two layer path vs. tuple is problematic. NAT rebinding within this and not new path difficult to reason about. Client might change path completely. Works in QUICv1, but different path.
        * No real strong conclusion: pros and cons, come up with different approach. Continue on github.
* Next steps

### Reliable Stream Resets

* 20 min - Open issues, updates to [Reliable Stream Resets](https://datatracker.ietf.org/doc/draft-ietf-quic-reliable-stream-reset/).
* [Slides](https://github.com/quicwg/wg-materials/blob/main/ietf117/reliable-resets.pdf)
* presented by Marten Seemann and Kazuho Oku

**Marten Seemann**:
* Diff since Yokohama
    * Kazuho joined as co-editor
    * (some discussion on slide versions)
    * renamed RELIABLE_RESET_STREAM to CLOSE_STREAM, because was confusing. If you implement it, it works more like a FIN with an error than a RESET, so settled on CLOSE_STREAM instead.
    * also added variant without error code, as requested
    * (waiting a long time on slide update. Awkward silence, as Marten hasn't gotten his stand-up comedy degree yet)
* Reliable?
    * in QUIC, if you reset a stream with some frames outstanding, you would not re-send the frames if they get lost
    * This extension is intended to declare a part of the stream (at the beginning) as reliable and then reset stream up to a certain reliable size. Everything up to that will be retransmitted, everything after won't.
* CLOSE_STREAM variants
    * 3 options for stream termination: No data kept = RESET_STREAM. Some data kept = CLOSE_STREAM. All data kept: STREAM with FIN bit
    * depending on stream API of your QUIC stack might or might not be awkward if you receive CLOSE_STREAM without error code. e.g., if you transmitted 100 bytes that have been received and you now get CLOSE_STREAM with reliable-size of 50 bytes. If has error-code, you can use that. If it doesn't, how do you signal to application? may or may not be problem in APIs
    * Editors struggle with this a bit. Have clear use case WITH error code, but not WITHOUT. Difficult to design without clear use case. Unless concrete feedback from room, we would remove the variant without error code.
* frame type size
    * ok with just using a 1-byte frame type?
    * **Martin Thomson**: no objection to 1, fine with 2 as well. We have plenty, not using at any great rate.
    * **Alessandro**: 1 byte is fine. Especially in QUIC where we don't have many colliding numbers due to extension negotiation.
    * **Marten**: yes, but they are also IANA registered, so we can get doubles.
    * **Lucas**: As individual: 1 byte is fine. As chair: think a bit more as a WG which things get priority for the lower numbers (maybe in a few years time?).
    * **Martin Thomson**: fine to keep using the lower codepoints; transport params will help differentiate. Main problem if people want to use different versions of the same extension at the same time. Will deal with this when things change.
    * **Martin**: In WebTransport/MoQ, this will be used A LOT, so argues for 1-byte codepoint as well.
    * **Lucas**: good to hear that from you, I had similar thoughts
    * **David Schinazi**: what are you doing for TP, how many bytes?
    * **Marten**: would like to get small value there, 1 or 2 bytes
    * **David**: makes sense. for VNEG we waited late in the process until WG Last Call to move to lower values. Do that for the ERROR code at the same time as the TP.
* Name of the Frame
    * Keep CLOSE_STREAM, go back to RELIABLE_RESET_STREAM, ...?
    * If you have opinions, send it to list please
    * **Martin Thomson**: that's a bike AND a shed, not necessarily a bikeshed
* Next steps
    * Prague: Ship -02 to incorporate feedback. After that maybe ready for WGLC
    * Would be nice to set some more interop. Currently between quic-go and quicly. Would be nice to have 3rd implementation.
    * **Lucas**: MT seemed to imply there are more people interested in interop/implementation, so please let us know. Don't see issues that would prevent this from proceeding though.
    * **David**: Webtrans enthusiast and chair: thanks to get this done so quickly. Not rushed, but still faster than expected. Only missing thing for WGLC is interop/implementation. Will follow with Victor to make sure Google implementation gets there.


### qlog

* 15 min - Open issues, updates to [qlog](https://datatracker.ietf.org/doc/html/draft-ietf-quic-qlog-main-schema).
* [Slides](https://github.com/quicwg/wg-materials/blob/main/ietf117/qlog.pdf)
* presented by Robin Marx

* Updates
    * Version upped
    * Extension RFCS
    * early Secdir review, nits fixed
* Breaking changes
    * Categories were too high level
    * Renamed
    * Will continue, hold off on implementing
* Extensions to support RFC 9287, 9220, 9218
* Less easy: RFC 9221 +RFC 9297
    * What is a datagram?
    * Split data moved event because 2 kinds of data
* How to log UDP level info
    * Issue with having two kinds of info now
    * **Martin Duke**: new UDP namespace in the quic document. Maybe inside baseball, but if later UDP QLOG module, would then have to reference this doc.
    * **Robin Marx**: yes, have to reference, some overlap but OK from h2 experience
    * **Martin Duke**: nevermind, don't want to tip over cart that badly
    * **Lucas Pardue**: if you're volunteering to do that, but with these urns can have additional schemas easily.
* Versioning
    * Use urn:ietf:params:qlog:quick-events-06
    * IANA register for extensions
    * Idea from RTP
    * **Lucas Pardue**: Doesn't seem terrible, if people strong opinions against come up, but this can work. Key to extensibility.
* Removal of .well-known:
    * Taken out and put on a new draft if people want it
    * Existing conflicting proposals
* Multipath support:
    * Current: includes PATH_CHALLENGE+PATH_RESPONS, not PathMigrationStarted/Stopped, IP addrs
    * Plan: add opaque path_id
    * Question: is this good enough? does it help with interop
    * **Mirja Kuehlewind**: Given where draft is now, how about just connection ID as top level field?
    * **Lucas Pardue**: Lurking at hackathon on multipath, something to visualize nice. Let's talk offline to drive design
    * **Christian Huitema**: Willing to help there, issue isn't path_id but editing tools to pass path specific acks etc. Make sure we have enough info qlog so that qviz could handle
* Qpack is coming


### ACK frequency

* 10 min - Open issues, updates to [Acknowledgement frequency](https://datatracker.ietf.org/doc/html/draft-ietf-quic-ack-frequency).
* [Slides](https://github.com/quicwg/wg-materials/blob/main/ietf117/ack-frequency.pdf)
* presented by Ian Hewett
* Updates
    * new error code, PMTU may use intermediate ack, removed a MUST and SHOULD.
* One or two byte frametype:
    * IMMEDIATE_ACK frequent, ACK_FREQUENCY less often, so make it 2 bytes
    * Should we do this?
    * **Martin Thompson**: 3 times per connection, don't use prime real estate
    * **Christian Huitema**: ACK_FREQUENCY depends on RTT, RTT changes, so updates with window updates. Most connections don't go out of start. Could do with 2 bytes.
    * **Kazuho Oku**: use
    * Conclusion: Change to two bytes
* IMMEDIATE_ACK after app-limited
    * If one ACK per RTT could send for 2 w/out an ACK out of quiescence
    * Technical solutions
    * Options: do nothing, editorial, RECOMMENDED
    * **Mirja Kuehlewind**: Disagree slightly: general issue. Connection is we have a mechanism that can help and recommend immediate ACK could be used. Not interop so no normative language required.
    * **Gorry Fairhurst**: Don't like do nothing, think generate ack somehow, not prescriptive on how
    * **Christian Huitema**: No normative statement saying "send the ACK", so many implementation cases that they can do it.
    * **Martin Duke**: Do something. Editorial vs. RECOMMENDED is how show. Often intuition is wrong in congestion. If we have data to support recommend, otherwise don't give ones that can be wrong.
    * **Martin Thompson**: Any recommendation is on receiver. Send the ack after being quiet, don't worry about it. 9002 should have said it. We should have text shape is about receiver not sender.
    * **Gorry Fairhurst**: Got it wrong because we didn't think about ACK dilution. Should describe it well.
* Deployment experience
* Takeaways
    * need PTO with IMMEDIATE_ACK with reordering
    * Careful with MinRTT, SRTT/4 is "good enough"
    * Reordering threshold ACKing not useful
    * ACK_FREQUENCY works
    * Normative text: say so on issue, otherwise nonnormative
    * **Matt**: Don't think byte size matter, good summary of data

### QUIC-LB

* 5 min - Open issues, updates to [QUIC-LB](https://datatracker.ietf.org/doc/draft-ietf-quic-load-balancers/).
* [Slides](https://github.com/quicwg/wg-materials/blob/main/ietf117/lb.pdf)
* presented by Martin Duke
* Long time deploy is hard
    * Turns out Google is big
* First octet:
    * 4 codepoints for rotating configs, one fir unroutable
    * Everyone gets new before the next one starts
    * Load balancer prev, current, next at once
* proposal:
    * 3 bits for config rotation, CID len 5 bits
    * Hardware people need some self-encoding length, otherwise random
* Why?
    * Can't guarantee everyone gets config before the next one rolls out
* Why not?
    * 32 byte CID limitation to self-encode
    * Attractive nuisance
* Multiple customers on IP via ECH, also quic-LB
    * How to route to backend? Give everyone same keys
    * Use config id per customer: defeats purpose
* Comments?
    * Misconfig is that misrouting happens, which does SRR, which might not work. Pass at what happens in chrome. Maybe handshake timeout.
    * **Kazuho Oku**: just do it
    * Will land next months after more ops experience

### Service Differentiation

* 10 min - [QUIC-enabled Service Differentiation for Traffic Engineering](https://datatracker.ietf.org/doc/draft-zmlk-quic-te/)
    * presented by Yunfei Ma
    * Problem solving: premium path for low latency, bulk transfer regular
    * Goal: balance cost and performance
    * Critical data over premium
    * Service differentiation by stream
    * Loss recovery or handshake packet
    * Proposal multipath plus priority in path CID
    * Schedule packets in the routes
    * Edge router pars and does SRv6, MPLS
    * Difference from current multipath: multiple last mile links. Here just one in backbone
    * Benefits Stream and packet level differentiation
    * User space has control in scheduler
    * Packet reordering, RTT estimation, path congestion control handled by multipath
    * QoS not middlebox interferable
    * Standardized to encode, coexist with server encoding, negotiation, number supported

**Watson Ladd**: seems that 1 network between client and server, but that's not how it works. Multiple different ones. Likely that reversed path is not known. Other thing: by having a coding, the obfuscation for privacy, by differentiating per stream, expose more about what traffic is flowing, so needs to be properly defined.
**Zhilong Zheng**: *(didn't catch this during note taking)*
**Ted Hardie**: 18 different things wrong with this, go back. Explain why do this in single connection vs multiple with DSCP. singe SRv6, can't trust DSCP why trust this, coordination with servers and orchestrations is gigantic operational pain you won't want
**Marten Seemann**: Ted made good points
**Alex ... (Google)**** : Frame not packet, use GRE if you don't. Why is server far in the network? Move it closer. Agree with everything
** David Schinazi**: Architecture enthusiast. +1 to what's been said before. Sounds a lot like application-aware-networking stuff that was proposed and still ongoing on list. Think they're trying to refine problem statement. Don't see recurring need to push this info on the network; too many privacy problems. First understand that. Agree QUIC is the best place, but first look at concept before we look into encodings.
**Gorry Fairhurst**: +1 for Ted. Transport enthusiast: also see multipath. Brings too many things into 1 draft.
**Martin Duke**: connection ID enthusiast: clarifying question: have commonly known codepoints or per-network custom mapping?
**Zhilong**: custom mapping, Not like DSCP, per-connection: you have multiple streams with different paths. So no separate registry.
**Martin Duke**: modulo good idea, can fit in. Load balancer is a router, do have multiple tiers if you configure it right. Discussion how it works
**Richard**: everyone before me has stolen my thunder, +1 to that. Unclear what the problem statement is and how to integrate with infra.
**Altanai**: A lot of statefullness. For every application own is important.
**Zhilong**: application understands priority
**Altanai**: but what if app says "everything is high priority"? backend-service provider has no control of what app demands?
**Zhilong**: server-side and infra-side works together .Have some knowledge which streams should be prioritized. If you don't, fallback to default settings.
**Spencer Dawkins**: Ted Hardie enthusiast, and also learning from the past. Path aware networking 9049 talks about obstacles here. If you do take Ted's advice several obstacles listed that apply here. Not fatal, need to be aware think about how to overcome them because they are real. Was editor for this RFC. Happy to talk about this at length.
**Christian Huitema**: Third party enthusiast. Application is that network is outside. If you are going to multipath much simpler way. As soon as you have expensive path and way to expose it, add PATH_STATUS that says what its for. Then endpoints decide what goes there.

### NAT Traversal

* 20 min - [QUIC NAT Traversal](https://datatracker.ietf.org/doc/draft-seemann-quic-nat-traversal/)

* **Marten Seeman**:
* v1 server reachable, client NAT'able
* Client might migrate actively
* ICE penetrates NAT via compare candidates, send through, compare and pick
* This draft says how to use QUIC in P2P setting
* uses: WebRTC over QUIC, lots of P2P protocols
* 3 modes, External signalling (ICE+QUIC) or combine them via connection migration
* Exchange candidates in QUIC, probe instead of connectivity, migration means we know how to pick, we know how to keep pairs alive
* Start with proxied quic, then migration probes candidates, them migrate to candidate. Server has to probe out as well.
* Do we need multipath? Not necessarily, but would be nice
* What's next?
* Interest, -00, lots of work.






# QUIC Working Group Minutes - IETF 97

*Scribed by Magnus Westerlund*


* [Meeting chat](xmpp:quic@jabber.ietf.org?join)
* [Meetecho](http://www.meetecho.com/ietf97/quic) remote participation
* [Minutes](hhttp://etherpad.tools.ietf.org:9000/p/notes-ietf-97-quic)

All times in KST.

## Tuesday, 15 November 2016

_9:30-12:00, Grand Ballroom I_

### Administrivia

* 2 min - Blue sheets / scribe selection / [NOTE WELL](https://www.ietf.org/about/note-well.html)
* 3 min - Agenda bashing

Chair Lars Eggert notifies the WG that this is going to be a boring meeting, per design. Chair Mark Nottingham showed the Note Well. 

No bashing of the Agenda.

### Charter Overview

_~30 minutes_

Review [our charter](https://datatracker.ietf.org/wg/quic/charter/) and discuss as necessary.

The chairs started the charter review. The purpose is to ensure that there is good understanding of the WGs charter, and to avoid issues related to this in the future. 

Noted that charter says enable multipath, there is yet no deliverable. But there are some raised extensions that should be considered as the base architecture is developed.

Eric Rescorla asked what does the charter text on network management means? The WG need to undestand what work is needed. Spencer Dawkins (AD) explained that the WG needs to consider the topic. Jari Arkko (chair of IESG) that the topic needs be discused in the WG. Mirja added that aspects of the discussion can go into the applicability and management statement for the protocol. Benoit Claise clarified that operators want to have advice on how they will be able to do management of the protocol. One person on jabber commented that the shown slide on network management charter part is a non sequitur. None of the current practices that QUIC is going to ignore deal with the tensions described in 7258.

Chair: document adoption does not mean it cannot change. It is a starting point.

### Planning

_~45 minutes_

Discuss how the group will meet its charter, including (but not limited to):

* Deliverable timings
* Editor appointments
* Issue tracking and resolution
* Meeting planning
* Implementation expectations and interop testing

The chairs explained that there will be a interim meetings between each IETF meeting, i.e. January [0], June, and Sept/October. The WG has a very agressive time schedule, to bound the time the people committing the time to do the work. The intent is to have remote attendance possibilities for the Interim meetings. 

The WG will use GitHub following the model of HTTPBIS. See slide 17 (Getting Started (2)) for links. There is explanation of method of working on GitHub. 

Jeff Hodges raised the question if the WG would use the W3C mailserver for gatewaying. The answer is no.

Please sign up for the interim in January earlier rather than later. The other two interims will one be in North America and one in Europe.

[0] https://mailarchive.ietf.org/arch/msg/quic/SxWbqUbfJ6qBWOpnTfY_C4bIWc8

### Drafts

_Balance of time_

Discuss the suitability of the input documents for adoption by the WG for its chartered deliverables:

* [draft-hamilton-quic-transport-protocol](https://datatracker.ietf.org/doc/draft-hamilton-quic-transport-protocol/)
See: https://www.ietf.org/proceedings/97/slides/slides-97-quic-quic-00.pdf. 

Jana speaking about the core specification and what discussion that has been happening so far. The intention is not to conclude on these topics, simply review them. 

Topics raised include, packet numbers, endian-ness, versioning, etc. See slides.

Spencer asked how many have read the draft, a show hand showed a significant part of the room had done that. 

Humming if this is a suitable starting point. A strong consensus for WG adoption (in person and in jabber).

* [draft-iyengar-quic-loss-recovery](https://datatracker.ietf.org/doc/draft-iyengar-quic-loss-recovery/)
See: https://www.ietf.org/proceedings/97/slides/slides-97-quic-loss-detection-and-congestion-control-00.pdf.

Ian Sweet presenting.

Martin Duke commented that he got the impression, that there appear to be a lot of variability of the control information. Please clarify what information that are accounted. A second comment is that there is a lot of pseudo code that is good, but the reference are confusing. Please clarify that they are informational background. Unless a function is atomic imported, then specify the algorithm normatively in the QUIC document. Marcelo agreed. Jana commented that it is difficult to import TCP, as the algorithms are not specified seperate from the wire format. 

Martin Duke, asked is there a plan for pluggable congestion control. Yes, but there will be an example. Or rather one standard congestion control algorithm. Currently that is new reno (https://tools.ietf.org/html/rfc6582), but cubic (https://datatracker.ietf.org/doc/draft-ietf-tcpm-cubic/) will soon be a possibility. Martin raised the question if there should be described requirements on congestion control. 

? asked if the loss recovery bound to a congestion control or globally available. It should be global. 

Who has read the draft? A solid representation some 15% of the room. 

Should the WG adopt the document: Strong consensus for adopting, some against. No one was willing to stand up and explain why they where against. Chairs commented, that it would be helpful if people could provide that feedback on the mailing list. There will be confirmation on the list. 


* [draft-thomson-quic-tls](https://datatracker.ietf.org/doc/draft-thomson-quic-tls/)
See: https://www.ietf.org/proceedings/97/slides/slides-97-quic-quic-tls-00.pdf.

Martin Thomson presenting the slides. 

Chair asked who had read the slides: Substantial fewer than the previous but still quite a number.

Martin Duke commented that editorial the document would be easier to use if was specified so that TLS 1.3 was a black box. 

Hannes asked about the design choices. Before there has been changes to TLS, where the record TLS layer is changed. This is not done on Stream 1, but the rest of the streams have a different record layer. Hannes concern is that the implementation appears to become very entwined. This relates to the previous comment on being able to drop in an TLS implementation. EKR commented that the proposed solution looks implementable, but haven't done it yet. It might be possible to have an align structure between. Russ Housley commented that it would be good to only AEDA algorithms, and nothing else to have well defined interface to the record layer. 

Discussion what attacks are possible against this proposal. Topic raised by Subodh.

Hum for adopting the document:  Very strong support, none against. 

* [draft-shade-quic-http2-mapping](https://datatracker.ietf.org/doc/draft-shade-quic-http2-mapping/)
See: https://www.ietf.org/proceedings/97/slides/slides-97-quic-http2-semantics-over-quic-01.pdf

Mike Bishop presenting the current design proposal, and raising some issue with the current design. A possible other way would be to do a new mapping for HTTP over QUIC. There are also other possibilities that will need discussion. 

Mark Nottingham, asked ?,  Mike answered 

Who has read the draft: Still a fair number, but less than the other documents. 

Spencer Dawkins asking an individual questions: What are HTTP/2 Extensions, headers or something else. H2 can define new extensions. There has been a couple of extensions. There will likely be a couple of more the coming next years. 

Jana arguing for adopting the draft. There should be work done to use the QUIC mechanism to make this simpler and cleaner. 

Ted Hardie asking about if there is an assumption that a single QUIC connection will only carry one application layer. Suggests that this should be discussed and moved out of the HTTP/2 document and put somewhere else. Mike responded, that this is interesting. One implication would that you can't rely on getting a particular stream. Also Upgrade could be used more flexible to use a protocol over a stream. 

Partick McManus, the bar bof for DNS over QUIC was announced (when?). 

Martin Thomson it is great that we have a lot of talk. Please adopt the document to have something to stand on. Jana seconds that.

Jana, commented that the negotiation should be in this document.

Eric Rescorla, argued that this document is mostly TODOs, and the benefit of getting editors lined up. 

Martin, we do need to work on HPACK. We likely need different documents for that. 

Hum for adopting: Strong support, some few against. Chairs noting that adopting this really as starting point. 
Russ Housley noting that he hummed against due that the WG should make a decision about the big fork before adopting anything. 

Julian Reschke how will this handle future versions of HTTP? As this is adopting HTTP/2 it is not obvious how one goes to a new version. HTTP over TCP can always fall back to HTTP/1.x. 

Mirja, commented that it would be good to have the fresh mapping document. 

Brian Trammel commented that it is important there is agreement between QUIC and HTTP communities. 

Jana noted this is not the only fork in the road we will see. 

Martin Duke, asked if there is a proponent for the new mapping. Martin Thomson commented, that he rather see an adopted document, and having the editors in place. 

Phill Hallam-Baker: I think it is a mistake to think of there being a 'HTTP' mapping at this stage. The needs of web browsing and web services have diverged. Web services don't need 90% of what is in HTTP but they do need MUX.

The chairs are going to discuss and then confirm the adoption on the mailing list. 

Document Editors proposed by chairs are:

Core: Jana and Martin Thomson
Loss Recovery: Jana and Ian Sweet
TLS Martin Thomson, Sean Turner
HTTP Mapping: Mike Bishop


### Parking Lot ("if time permits")

* Brian Trammel, [draft-trammell-plus-statefulness](https://datatracker.ietf.org/doc/draft-trammell-plus-statefulness/) and how it might apply to QUIC (5 min talk, 10 min discussion)

Joe Hildebrand asking if there is any people in the room that builds the boxes that would use the information and can comment if this is sufficient. 

Ian Sweet commented that today there are a lot of double ended closes that removes states. 

?: All the information would be integrity protected. Public Reset is non-authenticated, that is a problem. With QUIC some type of boxes dropping state would not be an issue, if the public reset is used to note the need for re-establish the state in the middle. 

What are the consequences of enabling this proposal? 

Yoav, in TCP it is obvious what a connection is. For UDP not so much, but flows can be found.`  Firewalls would drop packets that are out of state. 

Mirja, if there 

Stewart Cheshire, today my iPhone has long lived TCP connections. If an attacker sends a reset, then I will not receive push messages or iMessage etc. There is an issue here, how bad I don't know.

EKR confirmed that this is a proposal for addition. What are the benefits of this proposal for the endpoint. The endpoint can't determine that it is behind a NAT/FW that supports such a mechanism like this proposal. 

Tommy Pauly : It is hard to know if the network is doing this. But there are cases you can know this. Determining which network you are on. In the longer run, this will be more useful. We will need to ensure that this works well for multipath.

Jana: Do we have an implementor that will implement this. It is hard for endpoint to implement against this. Why are IETF doing work if the endpoint is not reading our RFCs and implementing them. 

Tim Shepherd: This WG should not discuss this, an future BOF would be the right place. The issue Eric Rescorla raised has not been that discussed. 

Spencer Dawkins, as the AD that closed BEHAVE WG. Thanks for having the discussion in this WG. This is part of the management discussion that you need have. 

Mirja, disagree with Jana that there is no FW/NAT vendor reading our documents.  There has already been some vendors indicating that there are interested in implementing state management for QUIC. 

* Endian Issues (Martin Thomson)
See: https://www.ietf.org/proceedings/97/slides/slides-97-quic-quic-endian-00.pdf

Brian Trammel: Make a meta comment. There is a performance benefit of being little endian. Likely zero. There are debugging issues with mixing big and little endian. We can produce numbers for what benefits. 

Jana: Point out the history here. Little indian was chosen due to which machines they where running on. 

EKR: There are a lot of variable length field in QUIC. This requires marshalling and conversion anyway so there is little benefit of using little endian. 

From jabber: is QUIC supposed to work on a big endian machine or should it just fail? Assuming work then there needs to be conversion routines and that being the case why not just follow the convention.

?: Something about TLS record layer? 

Hum: A very clear hum for big endian, only a little support for little endian. 

In room decision to use Big endian. To be confirmed on list. 


* QUIC Identifiers (Martin Thomson)
See: https://www.ietf.org/proceedings/97/slides/slides-97-quic-quic-identifiers-00.pdf

Eric Rescorla: The version has to bee echoed in the TLS handshake. The issue tying the ALPN version to the QUIC transport version. Don't want to have these bound, there should be orthogonal. 

Ted Hardie: Supports that these are orthogonal version. Martin responded that if you change the transport you may affect the upper layer. Ted responded that it is only an issue if that affects the properties that the upper layer needs. 

Mike Bishop: We want things simple, but not simpler than necessary. We need to state which application that is using the QUIC connection. There are two fields. Martin commented that one is unauthenticated, thus we need a third one. 

Jana: 
Martin, to resolve this we can 

EKR: 
    
Mike Bishop: There is not only draft version. What brought us ALPN, was HTTP/2. We don't want to have every different upper layer bound to different transport versions. Will require a lot to support. Not desirable. 

Let Mike know what proposed ALPN identifier the HTTP/2 over QUIC should use. 

Question, what about versions of QUIC or TLS etc. There are no semantic order in the ALPN field. 

EKR: The ALPN field is to identify what is ontop of QUIC. 

Transport version proposal:
    
Eric Rescorla: The right number of bits are 32. We should have a light weight mechanism to register the different experiments. What are not mentioning, are they sequential. Martin: We should carve out a continous space for drafts.

Jana: The right number of bits are 31, one to tell that this is not QUIC. As you have to roll out both endpoints to experiment there is little risk for collisions. 

Martin: Proposal that we use a wiki while we develop the protocol, and then later a mechanism can be defined. 

Mark Nottingham: To do interop, nominate a draft version as an interop version. 

Chairs Conclude:
    
    If you have issues with proposed GitHub repository structure send emails.
    
    Please register for interim. 
    
    



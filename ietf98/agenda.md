# QUIC Working Group Agenda - IETF 98

* [Meeting chat](xmpp:quic@jabber.ietf.org?join)
* [Meetecho](http://www.meetecho.com/ietf98/quic) remote participation
* [Minutes](http://etherpad.tools.ietf.org:9000/p/notes-ietf-98-quic)


## Thursday, 30 March 2017

_9:00-11:30, Vevey 1/2_

### Administrivia

* 2 min - Blue sheets / scribe selection / [NOTE WELL](https://www.ietf.org/about/note-well.html)
* 3 min - Agenda bashing


### Chairs' Overview

_~5 minutes_

Brief status report on the Working Group, Tokyo Interim, and upcoming meeting planning.


### QUIC Applicability and Manageability Statement

_~15 minutes_

Discussion of our charter deliverable for an Applicability and Manageability Statement.

Proposals to consider for adoption:
* [Applicability of the QUIC Transport Protocol](https://tools.ietf.org/html/draft-kuehlewind-quic-applicability-00)
* [Manageability of the QUIC Transport Protocol](https://tools.ietf.org/html/draft-kuehlewind-quic-manageability-00)

Presentation by Mirja Kuehlewind.


### Working Group Drafts

_~60 minutes_

Discuss the recently published -02 WG drafts:

* [Transport](https://tools.ietf.org/html/draft-ietf-quic-transport-02) ([presentation](https://docs.google.com/presentation/d/1m72Z0Vt2Ruxxkq4DIzUr84Slv-cSosZA9ANSV1HAjFk/))
* [Recovery](https://tools.ietf.org/html/draft-ietf-quic-recovery-02)
* [TLS](https://tools.ietf.org/html/draft-ietf-quic-tls-02) ([presentation](https://docs.google.com/presentation/d/18ybWD1oHvcrGTuEWKbxiFf4oHwr6qRSnuXsn1VPPthg/))
* [HTTP](https://tools.ietf.org/html/draft-ietf-quic-http-02) ([presentation](HTTP-QUIC.PDF))

... including the issues they attempt to address. The editors will give presentations summarising
their current state.


### Open Issues

_~60 minutes_

Discussion of open issues.

#### Crypto

* [167](https://github.com/quicwg/base-drafts/issues/167) - Hash for unencrypted packets
* [227](https://github.com/quicwg/base-drafts/issues/227) - Encrypt the initial cleartext packets with a deterministic key

* [45](https://github.com/quicwg/base-drafts/issues/45) - Handshake protocol selection

#### Shutdown/Close

* [61](https://github.com/quicwg/base-drafts/issues/61) - Silent close
* [330](https://github.com/quicwg/base-drafts/issues/330) - Clarify meaning of CONNECTION_CLOSE

#### HTTP

* [81](https://github.com/quicwg/base-drafts/issues/81) - Split from HTTP/2 framing?
* [376](https://github.com/quicwg/base-drafts/pull/376) - Separate IANA registries

#### Not-Crypto

* [391](https://github.com/quicwg/base-drafts/pull/391) - Packet number echo with variable-length numbering
* [393](https://github.com/quicwg/base-drafts/pull/393) - Packet number echo with fixed-length, 32-bit packet and echo numbers  
* [269](https://github.com/quicwg/base-drafts/issues/269) - Packet Number Echo in Public Header
* [279](https://github.com/quicwg/base-drafts/issues/279) - Public Flags to Aid Troubleshooting

#### Misc

Time permitting only.

* [348](https://github.com/quicwg/base-drafts/pull/348) - Define "httpq"

* [248](https://github.com/quicwg/base-drafts/issues/248) - Exemption from congestion control
* [384](https://github.com/quicwg/base-drafts/pull/384) - Stream1 is not that special

* [267](https://github.com/quicwg/base-drafts/issues/267) - Server enforcement of 1280 octet packet size

* [128](https://github.com/quicwg/base-drafts/issues/128) - We have two things called "frame"

#### Connection ID

Discuss privacy issues.


### Parking Lot ("if time permits")

_If you would like to present something (on a time permitting basis), please contact the Chairs._

* [QPACK](https://tools.ietf.org/html/draft-bishop-quic-http-and-qpack-02) - Mike Bishop ([presentation](QPACK.PDF))
* [ECN Support in QUIC](https://tools.ietf.org/html/draft-johansson-quic-ecn-01) - Ingemar Johansson ([presentation](ECN.pdf))

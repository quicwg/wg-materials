
# Runsheet for Transport issues

_"Time Permitting" issues will be discussed if there is time and interest in doing so; they may be held to the end of the meeting, or deferred._


### Application Expectations / Requirements

* #74: [Application-defined error codes](https://github.com/quicwg/base-drafts/issues/74) **CC**
* #104: [Priority in QUIC Transport](https://github.com/quicwg/base-drafts/issues/104) **ND**


### Streams

* #146: [STREAM frame boundaries](https://github.com/quicwg/base-drafts/issues/146) **ND**
* #174: [Stream Reservation](https://github.com/quicwg/base-drafts/issues/174)

#### Time Permitting

* #175: [Unidirectional streams](https://github.com/quicwg/base-drafts/issues/175)
* #165: [Resetting Streams](https://github.com/quicwg/base-drafts/issues/165)


### Structural

* #183: [Abstraction of TLS](https://github.com/quicwg/base-drafts/issues/183) **ND**


### Version Negotiation

* #51: [QUIC version number scheme](https://github.com/quicwg/base-drafts/issues/51) **CC**
* #45: [Handshake protocol selection](https://github.com/quicwg/base-drafts/issues/45) **CC**
* #135: [DoS using Version Negotiation Packets](https://github.com/quicwg/base-drafts/issues/135) **ND**

#### Time Permitting

* #143: [Repeating Version Negotiation](https://github.com/quicwg/base-drafts/issues/143)
* #133: [Connection ID in version negotiation](https://github.com/quicwg/base-drafts/issues/133)
* #89: [Version negotiation gaps](https://github.com/quicwg/base-drafts/issues/89)
* #112: [Greasing version negotiation](https://github.com/quicwg/base-drafts/issues/112)
* #121: [Version downgrade vulnerability](https://github.com/quicwg/base-drafts/issues/121)


### Settings and Other Handshake

* #50: [Updating transport parameters](https://github.com/quicwg/base-drafts/issues/50) **ND**
* #181: [Remove SETTINGS/SETTINGS_ACK](https://github.com/quicwg/base-drafts/issues/181) **ND**
* #49: [Transport parameter advertisements](https://github.com/quicwg/base-drafts/issues/49) **ND**
* #122: [Define transport parameters](https://github.com/quicwg/base-drafts/pull/122) **PR**
* #124: [Alt-Svc quic version hint](https://github.com/quicwg/base-drafts/issues/124) **ND**
* #126: [Separate transport parameters for 0-RTT](https://github.com/quicwg/base-drafts/issues/126) **ND**
* #117: [SCUP](https://github.com/quicwg/base-drafts/issues/117) **ND**

#### Time Permitting

* #116: [Each COPT might be better as empty transport parameters](https://github.com/quicwg/base-drafts/issues/116)
* #167: [Hash for unencrypted packets](https://github.com/quicwg/base-drafts/issues/167)


### Retransmission / Loss

* #66: [Remove STOP_WAITING](https://github.com/quicwg/base-drafts/issues/66) **ND**
* #57: [Advice on STOP_WAITING](https://github.com/quicwg/base-drafts/issues/57) 
* #63: [ACK retransmission](https://github.com/quicwg/base-drafts/issues/63)
* #114: [STREAM retransmission priority](https://github.com/quicwg/base-drafts/issues/114) **CC**

#### Time Permitting

* #157: [Updated information in retransmitted frames](https://github.com/quicwg/base-drafts/issues/157)
* #177: [Reliable transmission of CONNECTION_CLOSE](https://github.com/quicwg/base-drafts/issues/177)


### Connection IDs

[Discussion input](https://docs.google.com/document/d/16vHie4Qe44-SKZzxNzL4cClbCKqO7P3B-DYEAFRgWGs)

* #115: [Connection migration](https://github.com/quicwg/base-drafts/issues/115) **ND**
* #119: [Server-proposed connection ID](https://github.com/quicwg/base-drafts/issues/119) **ND**


### MTU

* #64: [Path MTU Discovery](https://github.com/quicwg/base-drafts/issues/64) **CC**
* #69: [Minimum packet size](https://github.com/quicwg/base-drafts/issues/69) **ND**

#### Time Permitting

* #139: [Minimum MTU](https://github.com/quicwg/base-drafts/issues/139)
* #164: [Padding handshake packets](https://github.com/quicwg/base-drafts/issues/164)


### Flow Control

* #163: [RST_STREAM and connection-level flow control](https://github.com/quicwg/base-drafts/issues/163)
* #162: [RST_STREAM and flow control](https://github.com/quicwg/base-drafts/issues/162) **CC**


### DoS / Reflection / Amplification / Misc Security

* #35: [Starting packet number](https://github.com/quicwg/base-drafts/issues/35) **ND**
* #52: [Source address validation](https://github.com/quicwg/base-drafts/issues/52) **ND**
* #120: [Source address validation](https://github.com/quicwg/base-drafts/issues/120) **PR**
* #118: [Source Address Token encoding](https://github.com/quicwg/base-drafts/issues/118) **CC**

#### Time Permitting

* #136: [First client packet size](https://github.com/quicwg/base-drafts/issues/136)
* #147: [Reflection Attack Resistance](https://github.com/quicwg/base-drafts/issues/147)
* #161: [Address change and consent to send](https://github.com/quicwg/base-drafts/issues/161)


### Format

* #40: [Variable-length fields](https://github.com/quicwg/base-drafts/issues/40) **ND**
* #148: [QUIC packet header complexity](https://github.com/quicwg/base-drafts/issues/148) **ND**
* #56: [Extending flags](https://github.com/quicwg/base-drafts/issues/56)
* #62: [Finding frame lengths](https://github.com/quicwg/base-drafts/issues/62)
* #70: [Move ACK/STOP_WAITING into the packet header](https://github.com/quicwg/base-drafts/issues/70) **ND**
* #108: [Maximum stream number](https://github.com/quicwg/base-drafts/issues/108) **ND**
* #109: [Time format](https://github.com/quicwg/base-drafts/issues/109) **ND**
* #123: [ACK frame timestamp format](https://github.com/quicwg/base-drafts/issues/123) **ND**

#### Time Permitting

* #158: [Inter-frame padding](https://github.com/quicwg/base-drafts/issues/158)
* #168: [Ordering of ACK Frame fields](https://github.com/quicwg/base-drafts/issues/168)


### Holding Tank

* #65: [BLOCKED usage requirements](https://github.com/quicwg/base-drafts/issues/65)
* #58: [Frame type extensions](https://github.com/quicwg/base-drafts/issues/58) 
* #61: [Silent close](https://github.com/quicwg/base-drafts/issues/61)  
* #68: [Explicit Congestion Notification (ECN)](https://github.com/quicwg/base-drafts/issues/68)   


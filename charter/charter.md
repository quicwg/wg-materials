# QUIC Working Group Charter

The QUIC WG originated the the specifications describing the QUIC
protocol, a UDP-based, stream-multiplexing, encrypted transport
protocol, and therefore acts as the focal point for any QUIC-related
work in the IETF. It is chartered to pursue work in several areas,
detailed below.

The working group will focus on maintenance and evolution of the
existing QUIC specifications and related documents:

- Maintenance and evolution of the QUIC base specifications that are
  describing its invariants, core transport mechanisms, security and
  privacy, loss detection and recovery, congestion control, version and
  extension negotiation, etc.

- Maintenance and evolution of the specifications of existing QUIC
  extensions, e.g., datagrams, etc.

- Maintenance and evolution of other QUIC-related specifications and
  documents, such as it applicability and manageability statements,
  improved operation with load balancers, etc.

Maintenance work needs to strongly be motivated by existing or ongoing
production deployments of QUIC at scale, and needs to carefully consider
its impact on the diverse set of applications that have adopted QUIC as
a transport.

The working group will also develop extensions to QUIC.  These
extensions need to have general applicability to multiple application
protocols.

The working group may also decide to publish QUIC extensions as
Informational or Experimental documents, e.g., to allow vendors to
publicly document deployed proprietary extensions or to enable wider
experimentation with new protocol features.

Specifications for how an existing or new application protocol will use
QUIC for transport need not in general be specified in the QUIC WG. The
WG will collaborate with other groups that define application protocols
that use QUIC. Extensions can also be defined outside of the QUIC WG
after review and consultation. In particular, collaboration is
recommended to reduce the chance that extensions do not duplicate
existing work, or do not interact poorly with other extensions when
deployed together.

Groups that define application protocols or extensions to QUIC in
support of those protocols are requested to consult with the QUIC WG and
seek review of proposals.

The QUIC WG originated the HTTP/3 binding to QUIC and the QPACK header
compression scheme. These specifications are now maintained in the
HTTPBIS WG.

Defining new congestion control schemes is explicitly out of scope for
the WG. New QUIC extensions allowing the development and
experimentation with new congestion control schemes may be defined as
part of the second work area.

# QUIC Working Group Charter

The QUIC WG originated the specifications describing version 1 of
QUIC, a UDP-based, stream-multiplexing, encrypted transport
protocol. 

The QUIC WG acts as the focal point for any QUIC-related
work in the IETF. It is chartered to pursue work in the areas
detailed below.

The working group will focus on maintenance and evolution of the
existing QUIC specifications and related documents:

- Maintenance and evolution of the QUIC base specifications that
  describe its invariants, core transport mechanisms, security and
  privacy, loss detection and recovery, congestion control, version and
  extension negotiation, etc.

- Maintenance and evolution of the specifications of existing QUIC
  extensions, e.g., datagrams, etc.

- Maintenance and evolution of other QUIC-related specifications and
  documents, such as it applicability and manageability statements,
  improved operation with load balancers, etc.

Maintenance and evolution work needs to be strongly motivated by existing
or ongoing production deployments of QUIC at scale, and needs to carefully
consider its impact on the diverse set of applications that have adopted
QUIC as a transport.

The working group will also develop extensions to QUIC.  These
extensions need to have general applicability to multiple application
protocols.

The working group may also decide to publish QUIC extensions as
Informational or Experimental documents, e.g., to allow vendors to
publicly document deployed proprietary extensions or to enable wider
experimentation with new protocol features.

Specifications describing how new or existing application protocols use the
QUIC transport layer do not need to be specified in the QUIC WG. The
WG will collaborate with other groups that define application protocols
that use QUIC. New mappings might require QUIC extensions and it may be 
efficient to define these alongside the mapping document. Groups that define
application protocols, or extensions to QUIC in
support of those protocols, are requested to consult with the QUIC WG and
seek review of proposals. This is intended reduce the possibility of
duplicate work and/or conflicts with other extensions.

The QUIC WG originated HTTP/3, the mapping of HTTP to QUIC, and the QPACK
header compression scheme. These specifications are now maintained in the
HTTPBIS WG.

Defining new congestion control schemes is explicitly out of scope for
the WG. New QUIC extensions allowing the development and
experimentation with new congestion control schemes are permitted.

# QUIC Working Group Charter

The QUIC WG originated the specifications describing version 1 of
QUIC, a UDP-based, stream-multiplexing, encrypted transport protocol.

The WG acts as the focal point for any QUIC-related work in the IETF.
It is chartered to pursue work in the areas detailed below.

The first such area focuses on maintenance and evolution of the existing
QUIC specifications:

- Maintenance and evolution of the QUIC base specifications that
  describe its invariants, core transport mechanisms, security and
  privacy, loss detection and recovery, congestion control, version and
  extension negotiation, etc.

- Maintenance and evolution of the specifications of existing QUIC
  extensions, e.g., datagrams, etc.

Maintenance and evolution work needs to be strongly motivated by
existing or ongoing production deployments of QUIC at scale, and needs
to carefully consider its impact on the diverse set of applications
that have adopted QUIC as a transport.

A second area of work for the WG is other QUIC-related specifications
and documents, such as it applicability and manageability statements,
improved operation with load balancers, the specifications of qlog
logging schemas, etc.

A third area of work is the specification of new extensions to QUIC.
These extensions need to have general applicability to multiple
application protocols. The WG may decide to publish such extensions as
Informational or Experimental documents, e.g., to allow vendors to
publicly document deployed proprietary extensions or to enable wider
experimentation with new protocol features.

Specifications describing how new or existing application protocols
use the QUIC transport layer do not need to be specified in the QUIC
WG. The QUIC WG will collaborate with other groups that define such
application protocols that intend to use QUIC. New mappings might
require QUIC extensions and it may be efficient to define these
alongside the mapping specifications. Groups that define application
protocols using QUIC, or extensions to QUIC in support of those
protocols, are requested to consult with the QUIC WG and seek review
of proposals. This is intended reduce the possibility of duplicate
work and/or conflicts with other extensions.

The QUIC WG originated HTTP/3, the mapping of HTTP to QUIC, and the
QPACK header compression scheme. These specifications are now
maintained in the HTTP WG.

Defining new congestion control schemes is explicitly out of scope for
the WG. New QUIC extensions allowing the development and
experimentation with new congestion control schemes are permitted.

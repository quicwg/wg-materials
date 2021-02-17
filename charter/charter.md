# QUIC Working Group Charter

The QUIC WG originated the specifications describing version 1 of
QUIC, a UDP-based, stream-multiplexing, encrypted transport protocol.

The WG acts as the focal point for any QUIC-related work in the IETF.
It is chartered to pursue work in the areas detailed below.

The first area of work is maintenance and evolution of the existing
QUIC specifications:

- Maintenance and evolution of the QUIC base specifications that
  describe its invariants, core transport mechanisms, security and
  privacy, loss detection and recovery, congestion control, version and
  extension negotiation, etc. This includes the specification of new
  versions of QUIC.

- Maintenance and evolution of the existing QUIC extensions specified
  by the WG.

WG adoption of maintenance and evolution work for the QUIC base specifications needs to be strongly motivated by
existing or ongoing production deployments of QUIC at scale, and needs
to carefully consider its impact on the diverse set of applications
that have adopted QUIC as a transport.

The second area of work is supporting the deployability of QUIC, which
includes specifications and documents such as applicability and
manageability statements, improved operation with load balancers, the
specification of a logging format, and more.

The third area of work is the specification of new extensions to QUIC.
The WG will primarily focus on extensions to the QUIC transport layer,
i.e., extensions to QUIC that have broad applicability to multiple
application protocols. The WG may also publish specifications to
publicly document deployed proprietary extensions or to enable wider
experimentation with proposed new protocol features.

Specifications describing how new or existing application protocols
use the QUIC transport layer need not be specified in the QUIC WG,
although they can. The QUIC WG will collaborate with other groups that
define such application protocols that intend to use QUIC. New
mappings might require QUIC extensions and it may be efficient to
define these alongside the mapping specifications. Groups that define
application protocols using QUIC, or extensions to QUIC in support of
those protocols, are strongly requested to consult with the QUIC WG
and seek early and ongoing review of and collaboration on proposals.
This is intended to reduce the possibility of duplicate work and/or
conflicts with other extensions.

The QUIC WG originated HTTP/3, the mapping of HTTP to QUIC, and the
QPACK header compression scheme. These specifications are now
maintained in the HTTP WG.

Defining new congestion control schemes is explicitly out of scope for
the WG. However, new QUIC extensions that support development and
experimentation with new congestion control schemes may fall under the
third work area.

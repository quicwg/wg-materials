The QUIC WG originated the specifications describing version 1 of
QUIC, a UDP-based, stream-multiplexing, encrypted transport protocol.

The WG acts as the focal point for any QUIC-related work in the IETF.
It is chartered to pursue work in the areas detailed below:

1. The first area of work is maintenance and evolution of the existing
   QUIC specifications:

   * Maintenance and evolution of the QUIC base specifications that
     describe its invariants, core transport mechanisms, security and
     privacy properties, loss detection and recovery, congestion control,
     version and extension negotiation, etc. This includes the
     specification of new versions of QUIC.

   * Maintenance and evolution of the existing QUIC extensions
     specified by the WG.

   WG adoption of work items falling into this first area of work
   needs to be strongly motivated by existing or ongoing production
   deployments of QUIC at scale, and needs to carefully consider its
   impact on the applications that have adopted QUIC as a transport.

2. The second area of work is supporting the deployability of QUIC,
   which includes specifications and documents such as applicability and
   manageability statements, improved operation with load balancers, the
   specification of a logging format, and more.

3. The third area of work is the specification of new extensions to
   QUIC. The WG will primarily focus on extensions to the QUIC transport
   layer, i.e., extensions to QUIC that have broad applicability to
   multiple application protocols. The WG may also publish specifications
   to publicly document deployed proprietary extensions or to enable
   wider experimentation with proposed new protocol features.

4. The fourth area of work is the specification of how QUIC stream
   multiplexing and other application-oriented extensions (e.g. Datagram)
   can be adapted to work over a reliable and bidirectional byte stream
   substrate. When the substrate is insecure, TLS will be the default
   security provider; no effort will be made to enable unprotected
   communication without a security provider. Deployments on a shared
   network must use a substrate that provides congestion control.

Specifications describing how new or existing application protocols
use the QUIC transport layer, called application protocol mappings
below, need not be specified in the QUIC WG, although they can. The
QUIC WG will collaborate with other groups that define such
application protocols that intend to use QUIC. New application
protocol mappings might require QUIC extensions and it may be
efficient to define these alongside the mapping specifications. Groups
that define application protocols using QUIC, or extensions to QUIC in
support of those protocols, are strongly requested to consult with the
QUIC WG and seek early and ongoing review of and collaboration on
proposals. This is intended to reduce the possibility of duplicate
work and/or conflicts with other extensions.

The QUIC WG originated HTTP/3, the mapping of HTTP to QUIC, and the
QPACK header compression scheme. These specifications are now
maintained in the HTTP WG.

Defining new congestion control schemes is explicitly out of scope for
the WG. However, new QUIC extensions that support development and
experimentation with new congestion control schemes may fall under the
third work area.

# QUIC Interim 2024-06-04

Notes: Martin Thomson, Magnus Westerlund

## Agenda

Mirja presented the initial agenda to talk about three main issues.

Lucas (as chair) presented the Note Well.

### Even odd/split:

[#328 Designing odd/even path-id, or not](https://github.com/quicwg/multipath/issues/328)

Mirja: _Note that the easiest solution would be to basically do nothing now because we can probably specify anything needed including the split with a new extension using a new transport parameter._

Mirja: We need to deconflict path ID allocation if we allow servers to open paths.  Lots of discussion, continued from last time.

Mirja: My view is that there is no reason not to allow servers to initiate paths.  Even if we don't, we could reserve half of the path IDs.  There might be other ways to deconflict.
... If both open with the same ID at the same time, there is a problem.  Maybe ok because a server can't migrate.
... If both allocate different path IDs for the same path, maybe that is OK.
... So maybe we don't need to deconflict.
... We could wait until later and use a new transport parameter to enable server-initiated path creation and do the reservation.

Christian: I agree with Mirja.  The motivation was not to foreclose on symmetric setups, but when I started doing a PR to allow that and it becomes long and intricate to do it correctly. It affects lots of details.  This is not something we should do as part of closing out the last issues.
... I suggested an alternative with odd/even splits.  Uses 31 bits instead of 32.  But not allow servers to use their half of the space.
... Server-initiated paths require additional machinery and transport parameters.  Therefore, this can be done as a new extension.
... If we do the work, we are largely speculating and we might make a mistake.

Mirja: Related to #332.  There is a way to allow server-initiated paths without new transport parameters.  Maybe we can do it right now.

Christian: we might do that, yes.  If we don't split IDs, we can use what we have now, but we have to find a way to resolve conflicts, which might be simpler or not.

Mirja: We should decide whether to do the split or not.

Martin Thomson: Thinks it is necessary to make decision, as there are interaction between even/odd and MAX_PATHS which is a count. This is still confused. Attempt to fix this in: https://github.com/quicwg/multipath/pull/372

Quentin: We need to have a way to determine who can create paths.  If we don't want to support server-initiated at all, that's OK.  If we want to support server-initiated paths and you want to have updates, we need to have a clear idea on how we can resolve conflicts.

Mirja: If we don't have a split, we can't limit the number of paths that each peer can open.  Maybe who opened it doesn't matter.

Christian: What I believe is that it is not a good idea to have asymmetry between server and client.  That will bite us when we do emulation of ICE where we need cooperation about who sends the first message.  That is a reason to not have the split.

Magnus: I wonder about what this has to do with MAX_PATHS and the potential for attack surface.  If either can increase it, then one could force the other to raise their value.  Does that open an attack surface.

Christian: The reason we had complexity was for exactly that reason.  WIth two MAX_PATHS, you still need to control resource allocation.  You need an agreement.  Otherwise you have an overflow of resources.  It's complicated.

Mirja: Path IDs are bidirectional, so you need both peers to open the limit.

Christian: MAX_PATHS really constrains the number of connection IDs that are in play.

Martin: I am now confused about what the limit is? Christian clarified that the current limit is the lower of both limits.

Mirja: Want to determine if anyone wants even/odd split.

Lucas: Was a big fan of the split in Brisbane because it fits with stream IDs.  It seemed more natural.  But I'm hearing that it creates more complexity.

Michael Eriksson: Think that if we are going for server initiated paths, then we should use an odd/even construction. But that can be done later when one writes an extension.

Martin: Unclear what the complexities are in regards how one uses a common path ID space. If one allow server initiated what happens if one endpoint consumes all available space, what does that mean for the peer?

Mirja: You can always create new paths and waste them or allocate them in suboptimal ways. But an endpoint can also refuse to allow a path to be opened by not responding to the path challenge.

Lucas: Conclude that for now we have a meeting consensus that we will not do the split. If we discover that this results in issues, we might have to revisit the decision with new information from implementation or work on specifying things.

There is an issue about server initiated path [#47](https://github.com/quicwg/multipath/issues/47)


### Reconsider the path closing procedure

[#313 When to CID expire if using Unique Path ID?](https://github.com/quicwg/multipath/issues/313)

Mirja: _the proposal is to change the closing procedure to retire CIDs immediately together with the path abandon (see issue for details)_

*Third discussed issue*

Mirja: Quite a bit of confusion about how to close a path.  PATH_ABANDON tells the peer not to use that path.  You wait 3PTO.  You might get a reciprocal PATH_ABANDON in that time.  At the end of that time, you retire any CIDs on that path.  Now you have to retire all of the CIDs, from both sides.

... Very much like closing a connection now.  This is not really necessary for multipath, because you always have another path to signal over.

Christian: Interop revealed that closing was ambiguous.  Once you abandon a path, you just don't care any more.  No point in retiring CIDs for abandoned paths.  People are lazy.  Laziness leads to a memory leak.  Prefer to say that if you abandon a path, all the CIDs go away.

Mirja: Thera are other resources also connected to the Path ID. Beyond CID one also needs to consider retransmission and ACKs to determine when things are done.

Mirja: The proposal is to require PATH_ABANDON in both direction. And then one doesn't need to send CID retirement.

Martin: Seems OK, just need to handle reordering here.  Will need to allow ACKs to travel on other paths.

Mike Bishop: We have to have a timer.  Though one side sends an abandon, those will result in a stateless reset eventually.

Michael: Out of order packets can produce a stateless reset in ordinary QUIC too.  You need a timer for sure. Implementation of single path QUIC also need to handle this when retiring CID and ignore the state less reset.

Christian points out in chat that stateless reset tokens are retired along with CIDs, which ensures that the reset is ignored.  The timer is just an optimization, so that we don't send stateless resets and so we don't discard packets.

Mike: ...

Christian: If you send an abandon, you have to keep the CIDs active until you receive an abandon.  You keep a draining period until that happens.

Magnus: The receiver of an abandon will drain its packets before sending its own path abandon. This can work fine.

RESOLUTION: Christian will write a PR.



[#366 Should we require explicit Abandon after path time-out?](https://github.com/quicwg/multipath/issues/366)

Mirja: _We already say SHOULD send abandon after time our or validation failure but it would probably make other issues easier if we do a MUST here to explicitly retire the CIDs related to this path ID_

Mirja: Proposes that an endpoint MUST send a path abandon if it doesn't want to use that path any more.

Yanmei: support MUST.  endpoints will have different idle timeouts.

[#318 Should path numbers be continuous?](https://github.com/quicwg/multipath/issues/318)

Mirja: _This is related because, having path IDs issued in order would make other issues probably a bit easier, so we should explicitly recommend that. However, we can probably not enforce it and therefore not rely on it._

Resolution: Yes, we should recommend continous path numbers.

### CID allocation strategy:

[#338 Clarify how new CIDs are allocated](https://github.com/quicwg/multipath/issues/338)

Mirja: _We now specify that the same path ID is used in both directions which could lead to a situation where each ends issues different path IDs and then no new oath can be opened. #318 is also related here because requiring the next in order path ID would avoid a mismatch but we still need to provide more recommendation about how many path IDs should be issued when._

Mirja: Stupid strategies can always shoot themselves in the foot. However, we want to recommend strategies that avoid some stupid misstakes. There are more aspects discussed in the issue.

Quentin: If one don't use a path ID, one still have the max_paths that limits.

Mirja: Recommendation to use in order, and if there are some irregularities then abandon the one. This to ensure that one can have usable path IDs where both endpoints have provided CIDs.

Mirja and Quentin attempted to work through an example. Clarify that one need to stay within the limit.

Christian: Making recommendations to use in order will improve interoperability and avoid strange behaviors.

Lucas: Conclusion is to write a better recommendation for CID allocation. Quentin to write a PR.



[#332 Should active_connection_id_limit be per path or per connection?](https://github.com/quicwg/multipath/issues/332)

Second issue discussed.

Mirja: _This issue is important in order to decide if we need to signal max paths to the peer or not which impacts the CID allocation strategy regarding how many path IDs should be issued._

Mirja: MAX_PATHS limits the number of paths.  The connection ID is the only state that you need to retain (along with a path ID).  The way to control the number of paths is MAX_PATHS.  You can also control the number of available paths by controlling how many connection IDs are available on each path.

Marten Seemann: You can have a path, but no connection IDs, which makes the path unusable.  This sounds like a bug.  Maybe we can do something like server preferred addresses.  So by opening a path, an endpoint has to provide a connection ID for that path.

Mirja: Confused.  Right now, you need to do both MAX_PATHS and MP_NEW_CONNECTION_ID.

Marten: No attack here, but the situation where a path exists but can't be used is complicated.

Martin: Like Marten's idea. But unclear what it does for the actual logistics in frame handling. Allowing for creating IDs out of order, or handling missing frames.

Mirja: If we limit CID we don't need the max_paths as that is implicit limited.

Christian: We have a habit of spending 6 mo exploring an option, then changing our minds and doing the same again.  This adds delays.

Mirja: Maybe we made this more complex than it needed to be.

Christian: Idea: CIDs are not in fact created when attached to a path.  What we do is we do that during PATH_CHALLENGE, then add a path ID along with that.  This is something we have been looking at for a while.  We need to guarantee that there is a CID available for the return communication path.  If we do that, I would agree that we might want to have a split between Path IDs (server/client).  That simplifies path management, but it creates more complexity about path abandonment (which ID to use in all signaling cases).  If CIDs are not attached to paths, it makes things like distinguishing rebinding more difficult.
... on the other hand, asking that CIDs are bound to PATH_CHALLENGE might solve this issue.

Yanmei: It is better that you have a separate CID limit per path.  #292 talks about this.  The path ID design requires a CID sequence be per-path as part of the mechanism.  Transport parameter for the active CID limit is for the path, we change it as we add paths.  if it is per-connection, we can waste capacity for new paths, which makes the CID allocation strategy harder.  That would make it easier for attackers to force memory allocation on one path.  I think it is easier to keep the CID limit on each path.

Mirja: There should be no attack in either case.

Magnus: Are you sure that you won't have CIDs that are specific to one entry point to the network.  If you have multiple addresses they could need different CIDs.

Mirja: Not about that.

Christian: Magnus are correct, that there are some addresses that needs bound CIDs to them.

Martin: When challenging on a particular path, you want to indicate which CIDs that would actually lead back to this address. We might end up in a situation where one provide an address and that would have limited set of path IDs and CIDs.

If we hand out a CID without any binding we might end up with CIDs that are used on the wrong path.

Mirja: If you are behind two load balancers you need to get them coordinated to ensure that they route correctly.

Christian: This is going into the woods. This case will not work for an RFC 9000 case either. It works because we assume that there is one path to the server.  Having multiple paths to the server is not in scope.

Lucas: Our servers pick CIDs.  Therefore this is a problem for servers.  At least in our infrastructure. It is not clear how this discussion is resolving.

Christian: I think we have consensus, which is to keep what we have now.  We need to limit CIDs.  We can have #Paths x #CIDs or just #CIDs.  Either works.  What we have works.

Mirja: Just saying that MAX_PATHS is more complex.  The change would be to remove MAX_PATHS and then we need to use connection ID limits to control what new paths can be opened.

Christian: The draft works, I've implemented as has Yanmei.

Mirja: Happy to move on.  Would record the outcome as "do nothing".  Maybe keep it open to ensure that people understand it.

Returning after more discussion on other issues:

Mirja: With a connection ID limit one doesn't need max_paths following a sane allocation structure. If one want to allow server side path initilization then one doesn't need a new frame or transport parameter as they would be constrained under a common limit for the connection.

Michael: Could we not just use Stream variant for limits?

Mirja: No, doesn't work as it allows for a client to allow a lot of paths and push CIDs to the peer.

Christian: A global limit of path IDs have the same property as global CID limit. One can use other mitigation with that limit without introducing more mechanisms.




# IETF-120 QUIC WG meeting

## Thursday, July 25, 2024

Note takers: Martin Duke, Marco Munizaga

# Hackathon report (see chair slide)

### Multipath QUIC (Yanmei Lu, Mirja Kuhlewind -- see slides)

Mirja: 13-15 issues remaining that have design implications. Hopefully we can get through them today.

##### Issue 359: Renaming frames

WG is weakly supportive of using PATH instead of MP in frame names

Mike Bishop: should be MAX_PATH_ID, not PATH_ID_MAX.

Mirja: file an issue

#### Issue 283: Rename PATH_STANDBY to PATH_BACKUP

Room is fine with it.

#### Issue 343: What if SPA migration fails?

Christian: This issue highlights something implicit: that MP basically replaces the migration mechanism in RFC9000. Should be more explicit about what we're keeping from 9000.

#### Issue 220 "SHOULD" use ACK_MP frames?

Kazuho: I would like MUST, but it's not a strong opinion.

Yanmei: Initial path could use RFC9000 ACKs, which makes it more compatible.

Mike Bishop: You have handle legacy frames in the handshake, so it doesn't save any complexity with MUST.

Christian: We can have a MUST after the handshake. A MUST means there is one less code path. Fewer tests, easier code verification.

Matt: Do other implementers think MUST simplifies things greatly?

Christian: It's a weak preference.

Matt: Is anyone opposed to a MUST?

Mike Bishop: MUST doesn't make sense.

Quentin: Implementing both was simple for me. But I would prefer not having a MUST.

Matt: Seems like there is weak support for a MUST.

Marten Seemann: RESET_STREAM_AT had the same discussion and decided to support both, so I support SHOULD.

Show of hands: an MP implementation MUST use ACK_MP frames after it is negotiated. Yes: 11, No: 11, No opinion: 28

Matt: No consensus for change, so keep it a SHOULD.

#### Issue 378: Guidance if multiple paths on one 4-tuple

Magnus: One reason to have multiple paths over the same 4-tuple is to have different QoS using different DSCP codepoints on the different paths. Thus, it might be worth pointing out this type of reasons for opening multiple paths.

Watson: Adding justification is good because I had no idea why you would want to do this.

Alessandro: What would the further guidance be?

Christian: The reason people do this because the 4-tuple doesn't totally identify the path. You have the IPv6 Flow ID, and DSCP.

Mirja: Does someone want to write something.

Gorry: We don't have to go overboard here. Just make the point and move on.

Kazuho: I agree with everyone else. My example would be port numbers.

#### Issue 253: Review Error Codes

Alessandro: A specific error code is better for debugging, but maybe not useful. I don't care that much.

Mirja: Let's remove it.

Martin Duke: No preference, but I feel like it's useful to have a different error for multipath. We have 2^62 codepoints.

Christian: there's a tradeoff between debugging and attacks. The returned error code enables attack by identifying te weakness.

Martin Duke: That's convincing, thanks.

Mike Bishop: We have a CONN_ID_LIMIT in 9000. But Christian's argument is convincing.

#### Issue 414: Abandon Frame needs Error Code definition

Lucas: Why would this be an Application error?

Mirja: Closing a path is an application action.

Lucas: I don't see why would use application codes.

Christian: We could split abandon-by-network from abandon-by-application. But there are few protocol/network reasons. There could be a magic number if it's a protocol reason.

Matt: So an MP-QUIC application would use a special code to tell its peer?

Kazuho: All application codes are reserved for the App. So the transport can't decide to send this frame.

Lucas: This is going to cause issues. I can port my H/3 app to use multipath. But now I need to figure out all these application errors.

Mirja: Should we just remove the error code?

Mike Bishop: Yes. Paths aren't really affected by the app data layer. Debugging is the only reason to send the error, so maybe keep the reason phrase.

Matt: Christian, do you think this is required for MP apps to have success? Could this be added later?

Christian: I am now convinced that the app doesn't want to provide a reason. Just delegate it to the protocol stack. So it is a QUIC error code.

Mirja: or no error code at all?

Christian: I can see a difference between no error, and I ran out of resources.

Matt: There are CONNECTION_CLOSE type things that are not fatal to the connection, like the socket failing.

Mirja: but a reason phrase might be enough.

Christian: all the equivalent frames have an error code. There is definitely NO_ERROR and OUT_OF_RESOURCE

Matt: e.g., you are repeatedly receiving a socket error, and you could put it in an error code.

Christian: I think we're deciding that if there's an error code, it's a QUIC error code.

Marten Seemann: reason code seems heavyweight. Have to check stream length, etc. Have APPLICATION_ASKED and PATH_FAILED.

#### Issue 342: MAX_PATHS_BLOCKED

Marten: sounds good, but please name it PATH_BLOCKED to be consistent?

Mirja: yes

#### Issue 312 PATH_STANDBY/PATH_AVAILABLE sequence nubmer spaces: one or per-path?

Alessandro: I don't see any benefit to change this.

Kazuho: All the number spaces should be per-connection or per-path, which means it should be per-path.

Mike Bishop: These are only processed in a path context. You could implement either way as long as they increase monotonically.

Mirja: You have to specify it, or numbers can be re-used.

Mike Bishop: we shouldn't overspecify

Mirja: no change is the decision.

#### Issue 303 Recommendation on Token ambiguity

Mike Bishop: Don't mandate what the server says. The client should use the most recent one.

#### Issue 362 "refusing a path" == "closing a path"

No comments

#### Issue 397 what to do on path idle timeout

Alessandro: Either say "MUST NOT use path" or send the Abandon frame. We have to say MUST or MUST NOT.

Mirja: sometimes you want to keep an idle path.

Alessandro: Then what is the point of idle timeout?

Mike Bishop: The point in 9000 is to close it silently. If all paths have idled out, the connection is closed. But for a path, there should be PATH_ABANDON on the next packet.

Mirja: But don't wake up to send it.

Christian: If you decide not to listen on a path, you MUST tell the peer (but can take your time in sending). The question is, if the peer knows you are running a timer, the peer will send probes. Do we want to warn the peer so that it can send probes? We don't want to require keepalives.

Mirja: But I can still use the path if I don't get PATH_ABANDON.

Lucas: This is very confusing. The rules for connection and path are different? I'll take a look and make comments.

Mirja: The difference is, there is always an explicit signal.

Lucas: Can you keep a path alive on a different path? I'll go to the issue.

Martin Thomson: Christian + 1. Idle timeout is connection state, not path. You have the means to report path state, use it.

Tianji: In a mobile environment, it's about power. Keepalives would mean that phones have to wake up. That's bad.

Gorry: MT + 1. There is mixup between live endpoints and path state.

#### Issue 390: Packets before PATH_CHALLENGE

Kazuho: We would have to add PATH_CHALLENGE to the whole first flight if it's an error.

Martin Thomson: PATH_CHALLENGE is for the sender to validate receipt by the receiver. We should not require validation from the other end of that. No requirements for would-be PATH_CHALLENGE receiver, no enforcement.

Mike Bishop: MT + 1

Christian: MT + 1. It's really a SHOULD. 9000 has more rules because it's one-path-at-a-time.

Watson: What is the scope of validation? Does it need to validate two paths to the same address?

Kevin Cox: You shouldn't send if the path isn't validated.

Martin Duke: It should be a MUST because there's no good reason to not validate the path, even if it's not enforced.

Martin Thomson: The requirement should be that the sender MUST have validated the path IAW RFC 9000, somehow

Martin Duke: I agree. and it's a MUST even though unenforced.

Christian: It ought to be SHOULD because we're not enforcing.

Gorry: Are we validating identity or connectivity?

Mirja: Decrypting the packet verifies identity?

### QLOG (Lucas Pardue -- see slides)

#### Issue 198 clock problems

Watson: Use timestamps, that's what they're for.

Lucas: We only care about relative times from start of connection, so that's unnecessary.

Martin Thomson: This is easier to debug with a monotonic clock. We should have an epoch timestamp and log has ms offsets.

Lucas: The epoch of a monotonic clock is opaque. People might think they can get an absolute time, and that is wrong.

MT: Monotonic clocks may not advance at the same rate, but 1 ms ~ 1 ms. But time 0 is the wall clock and the monotonic clock reference point.

Lucas: great until we have daylight savings

MT: The qlog says connection started at Time X from the wall clock. Then all events are relative to that. Not 100% perfect due to precision, but it's close enough.

Lucas: agreed. then they translate back to wall clock and correlate with other logs. welp.

MT: That's a problem that people are doing the wrong thing.

Kevin: You can only do so much to prevent stupid stuff.

### AD interlude

Zahed: Good progress on MPQUIC. Design issues are resolved. How far are we from being done?

Mirja: All undiscussed things are editorial. We probably need > 1 updates to fix all the editorial stuff. I hope to be done before the next meeting?

Matt: How is implementation/interop status?

Mirja: There are multiple interoping implementations, but not all the tests. We can get there by IETF 121.

Zahed: SGTM.

Mirja: If we have more issues, let's have a virtual interim before 121.

Altanai: As an observer. I don't see a lot of diagrams or anything about prioritization and scheduling.

Matt: Scheduling is out of scope. The authors are willing to accept diagrams but there are no plans to add any.

### Accurate ECN (Marten Seemann) -- see slides

Lars: How many bytes are we adding?

Marten: Depends how many markings there are.

Gorry: We don't know what the marking pattern will be. This can lead to a dangerous size explosion. I'm not sure the extra info helps.

Marten: EVery packet having a different marking is the worst-case scenario, but not realistic. Prague cares about size. Not sure why?

Mirja: TCP has the same problem. L4S/Prague informed RFC9000. Having a byte count would be much easier. But it's best to just extrapolate from averages.

Marten: What we have is not good enough. I still don't know what order to apply increase and decrease to cwnd.

Mirja: but the order doesn't matter?

Martin Thomson: A gap can be zero length, which is a format change. Independent of details, ECN markings carry information. They are effectively random. The encoding is not scalable if it is random.

Magnus: In mobile systems, a marking percentage is applied quasi-randomly, not on the packet that triggers congestion. So the signal precision here is not valuable.

Christian: Ranges will be short in the average case, so the ACK is huge. An adversary can blow up your ACK. I object to doing it just for ECN. There is also transmission delay. Marking rate is basically per packet, per byte. So this is not valuable information.

Matt: There is a draft for ack range transmission delay.

Christian: Ack frequency is better lever to reduce this ambiguity.

Lars: experiment with a QUIC extension

### H/3 Extensible prioritization in the wild

(Pointer to paper and ANRW presentations)

### QUIC token misdirection (Mike Bishop)

Martin Duke: I, as the client, wouldn't take the token to a new IP and expect it to work.

Mike: The problem is tokens normally don't fail the connection, but format confusion can lead to that here.

Q Misell: Extensible tokens could also solve this. Let's talk about it on list

Mike: It could make it a smaller problem

Kazuho: CONNECT-UDP could prevent the client from knowing the target CDN has changed.
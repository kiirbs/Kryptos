# RFC-KPT-0002
## Kryptos Identity Protocol

### 1. Status

Draft

---

### 2. Purpose

Define the Kryptos identity protocol.

---

### 3. Scope

This RFC specifies the Kryptos identity protocol. 

It defines:
- the Kryptos identity model;
- identity roots and operational components;
- authenticated identity events;
- the identity journal and event graph;
- event verification and resolution;
- current state reconstruction;
- propagation and re-evaluation rules;
- multi-machine synchronization;
- conflict detection and resolution;
- trust bootstrap and trust state management;
- the responsibilities of IdentityStore and TrustManager.

This RFC does not define:
- the binary `.kpt` container format itself;
- private key storage implementation;
- transport protocols;
- user interface behavior;
- network synchronization protocols.

---

### 4. Design Principles

- No redundant information
- Upward compatibility
- Separation of concerns
- Downward compatibility where possible
- Avoid inferable information
- Objects represent the concepts in the specification

---

### 5. Terminology

| Term | Description |
|------|-------------|
| `Identity ID` | Public identifier for an identity. |
| `Root` | Cryptographic identity authority. |
| `Component` | Operational key associated with an identity. |

---

### 6. Identity Model

#### 6.1 Identity ID

An **`Identity ID`** is a public, stable, and opaque identifier for an identity. 

It:
- is public.
- is non-secret.
- is stable.
- does **not** change during a root rotation.
- must **not** depend on the current root.

Identity ID is **not** a Root ID.
Identity ID is **not** a Component ID.

---

#### 6.2 Root

An **`Identity Root`** is a cryptographic identity authority. 

It has:
- Root ID
- Public Key
- Algorithm
- Private Key

Root private key **MUST** be secret and **MUST NOT** be stored in IdentityStore.

---

#### 6.3 Component

An **`Identity Component`** is an operational key associated with an identity:
- operational role
- permissions granted by delegation
- new component for a new key
- stable Component ID

---

#### 6.4 Trust State

A Cryptographic State is **not** a Trust State. 

Trust States are: 
- `UNKNOWN`
- `PENDING`
- `TRUSTED`
- `REVOKED`
- `CHANGED`

These statuses are managed by `TrustManager`, **not** `IdentityStore`.

---

### 7. Identity Objects

Global pattern: 
- Purpose
- Fields
- References
- Authority
- Validation
- Effects

---

#### 7.1 RootRecord

Definition:
- `Event ID`
- `Created At`
- `Root ID`
- `Algorithm`
- `Public Key`

Established the original Root for an identity. 
RootRecord is **not** necessarily the current Root.

The initial Root of an Identity is established by a self-authenticated RootRecord. The Root signs the canonical representation of its own RootRecord. Trust in the Root is established independently through TrustBootstrap.

The creation of an identity does **not** need to be validated by a global authority.

---

#### 7.2 RootSuccession

```text
    ┌──── SUCCESSION_OF <───┐
    ▼                       │
ROOT_A ->  SUCCESSION   -> ROOT_B
```

Definition:
- `New Root ID`
- `New Public Key`
- `New Algorithm`
- `Succession Type`
- `Effective At`
- `Context`

A `Root` **MAY** have multiple competing succession `Events` in the journal, but at most one successor branch may be selected as current.

Multiple valid competing successors create a `CONFLICT`.

For a `RootSuccession`, the `Issuer` **MUST** be the predecessor Root.

---

#### 7.3 KeyDelegation

Definition:
- `Component ID`
- `Role`
- `Permissions`
- `Issued At`
- `Expires At`
- `Context`

A `KeyDelegation` may remain historically valid while becoming inactive in the current state.

A delegation issued by a historical `Root` does not become invalid solely because that Root is no longer current.

---

#### 7.4 KeyRevocation

Definition:
- `Component ID`
- `Reason`
- `Revoked At`
- `Context`

When applicable, a `KeyRevocation` causes the current effect state of the referenced Component to become `REVOKED`.

---

#### 7.5 ConflictResolution

Definition:
- `Event ID`
- `Created At`
- `Conflict ID`
- `Resolution Type`
- `Selected Event ID`
- `Context`

`Conflict ID` identifies the conflict.
`Selected Event ID` identifies the selected branch.

---

#### 7.6 IdentityComponent

Definition:
- `Component ID`
- `Algorithm`
- `Public Key`
- `Parameters`

**`Issuer = Root`**

---

### 8. Identity Event Model

#### Event Structure :

> **Events are immutable historical facts.**

Verification state, resolution state, and current effect are derived states and are not part of the event content.

```text
KryptosEvent
├── Event ID
├── Event Type
├── Version
├── Identity ID
├── Created At
├── Issuer
├── Payload
└── Signature
```

- `Event ID`: identifier for an Event.
- `Event Type`: indicate the Event type.
- `Identity ID`: The ID of identity for which the event is valid.
- `Created At`: Creation timestamp.
- `Issuer`: Identifies the cryptographic authority that issued the Event.
- `Payload`: Content depends on the Event Type.
- `Signature`: Used to verify authenticity.

---

### 9. Identity Journal

#### 9.1 Event Graph

An `Event Graph` is a **set of immutable authenticated events**.

```text
IdentityEventGraph
├── Events
├── Dependencies
├── Dependents
├── Relations
└── Conflicts
```

The applicable dependency relationships **MUST** form a **Directed Acyclic Graph** (**DAG**). 
At least for the relationships used in causal resolution.

---

#### 9.2 References

References identify objects or events referenced by an `Event`.

References are type-specific and are defined by the `Event` payload.

Examples:
- `RootSuccession` references the previous `Root` and the new `Root`.
- `KeyDelegation` references the issuing `Root` and the delegated `Component`.
- `KeyRevocation` references the issuing `Root` and the revoked `Component`.
- `ConflictResolution` references a Conflict and a selected `Event`.

A reference **MUST** identify an element belonging to the same Identity ID.

An unresolved reference does **not automatically** make an `Event` invalid.
If the referenced element is required but has not yet been received, the `Event` may remain `INCOMPLETE`.

---

#### 9.3 Dependencies

A dependency represents a logical prerequisite required to determine the state or applicability of an `Event`.

Dependencies are derived from the `Event` type and its references.

Examples:
- `RootSuccession` depends on the previous Root.
- `KeyDelegation` depends on the issuing Root and the referenced `Component`.
- `KeyRevocation` depends on the issuing Root and the referenced `Component`.
- `ConflictResolution` depends on the referenced Conflict and selected `Event`.

A missing required dependency causes the dependent element to remain `INCOMPLETE` and/or `BLOCKED` until the required information is available.

A semantic reference does **not necessarily** imply a causal dependency.

---

#### 9.4 Causality

The logical order of the `Graph` does **not** depend on the order in which the data is received.

---

#### 9.5 Branches

It is normal for Components to have **multiple branches**.

---

#### 9.6 Conflicts

Multiple competing successions of `Root` cause a `CONFLICT`.

---

### 10. Verification

#### 10.1 Verification States

| Verification State | Description |
|--------------------|-------------|
| `UNVERIFIED` | The status has not yet been verified. |
| `INCOMPLETE` | The Event is structurally valid, but the evidence required to fully verify it is not yet available. |
| `VALID` | Verification is valid. |
| `INVALID` | The Event fails a mandatory structural, cryptographic, or protocol validation rule. |

---

#### 10.2 Verification Rules

```text
UNVERIFIED → INCOMPLETE
UNVERIFIED → VALID
UNVERIFIED → INVALID

INCOMPLETE → VALID
INCOMPLETE → INVALID
```

Any other change in state is **impossible**.

---

#### 10.3 Invalid Events

An `Event` in the `INVALID` state cannot transition to the `VALID` state.
The `INVALID` status means that the evidence could **not be verified**.

---

#### 10.4 Incomplete Events

The `INCOMPLETE` status means that the evidence required to validate the event has **not been provided** or is **insufficient**. It can change.

---

### 11. Resolution

#### 11.1 Resolution States

| Resolution State | Description |
|------------------|-------------|
| `BLOCKED` | Element blocked by a conflict situation. |
| `READY` | Everything is in order and ready to use. |
| `REJECTED` | Rejected due to a conflict. |
| `CONFLICT` | **State of the subgraph** representing a conflict. |

---

#### 11.2 Applicability

If a `CONFLICT` is unresolved, Events whose applicability depends on the conflicting branch are `BLOCKED`.

After a valid `ConflictResolution`:
- affected Events in the selected branch are re-evaluated;
- affected Events in the non-selected branch become `REJECTED`.

```text
No blocking CONFLICT → READY

If unresolved CONFLICT → All dependent events are BLOCKED

If CONFLICT resolution:
Selected branch events = BLOCKED → re-evaluated
Not slected branch events = BLOCKED → REJECTED
```

---

#### 11.3 Blocking

When there is a `CONFLICT` between two `Roots`, all `Events` that depend on those `Roots` are `BLOCKED` until the `CONFLICT` is resolved.
A `CONFLICT` is **a state of the affected graph or subgraph**.
It is **not** an alternative authenticity state of an `Event`.

---

#### 11.4 Conflict Handling

A `CONFLICT` occurs when two or more valid `RootSuccession` Events propose different successors for the same predecessor `Root`.

All competing Events remain part of the historical journal.
No branch is automatically selected.

---

#### 11.5 ConflictResolution

When a `CONFLICT` is resolved by the protocol, the `Events` in the selected branch change to the `READY` state, while those in the non-selected branch change to the `REJECTED` state.

---

### 12. Effects

#### 12.1 Effect States

| Effect State | Description |
|--------------|-------------|
| `UNKNOWN` | No informations about effect state. |
| `ACTIVE` | Effect is now active. |
| `INACTIVE` | Effect is now inactive. |
| `REVOKED` | The referenced Component or authorization has been revoked by an authorized authority. |

```text
VALID ≠ ACTIVE
VALID ≠ TRUSTED
INACTIVE ≠ INVALID
REVOKED ≠ INVALID
```

---

#### 12.2 Active

`ACTIVE` requires that **all conditions for applicability be met**.

---

#### 12.3 Inactive

`INACTIVE` does **not imply** `INVALID`.

---

#### 12.4 Revoked

A `REVOKED` effect state **cannot** be reversed implicitly.
A new protocol-defined authorized event would be required for any future state change.

---

### 13. Propagation

#### 13.1 Dependency Graph

Causal dependencies **are directed**. They **must not** form a cycle. 

---

#### 13.2 Reverse Dependencies

Causal dependencies are directed.

For efficient propagation, the `IdentityStore` maintains or derives a reverse dependency index allowing it to identify all Events that depend on a given `Event` or state.

Example:

`E4 DEPENDS_ON E2`

allows the store to query:

`E2 → E4`

---

#### 13.3 Re-evaluation

Ingestion of a new `Event` **MAY** change the derived state of existing `Events` or identity elements.

When a derived state changes, the `IdentityStore` **MUST** re-evaluate the affected dependents in the relevant subgraph. 

---

#### 13.4 Fixed Point

After ingesting one or more elements, the `IdentityStore` **re-evaluates** the affected subgraph until it reaches a **fixed point**: *a state in which no further application of the resolution rules produces any changes.*

---

#### 13.5 Cycle Detection

Before adding a causal dependency `A → B`, the `IdentityStore` **MUST** verify that `B` does not already depend on `A`.

If adding the dependency would create a directed cycle, the dependency **MUST NOT** be accepted into the causal dependency graph.

Cycle detection **MUST** be performed on causal dependencies only.
Semantic relationships do not automatically participate in cycle detection.

---

### 14. IdentityStore

#### 14.1 Responsibilities

`IdentityStore` is a **persistent store** and **state engine** for the public and verifiable state of known identities.

It:
- stores authenticated historical `Events`;
- reconstructs the Event Graph;
- resolves dependencies;
- detects conflicts;
- reconstructs the current `Root` and `Component` states;
- propagates state changes;
- re-evaluates affected elements;
- reports unresolved or conflicting state.

```text
API:

register_identity()
get_identity()

add_root()
get_root()
get_current_root()

add_root_succession()

add_component()
get_component()
validate_component()

add_delegation()
get_delegation()

add_revocation()
is_revoked()

get_identity_state()
verify_identity_state()
```

---

#### 14.2 Storage Model

`IdentityStore` maintains a persistent journal of authenticated public identity events.

The storage model consists conceptually of:

- an immutable `Event` Journal indexed by `Event ID`;
- indexes allowing lookup by `Identity ID`, `Root ID`, `Component ID`,
  `Conflict ID`, and dependency relationships;
- reverse dependency indexes used for propagation and re-evaluation;
- derived state that **MAY** be cached but **MUST** remain reconstructible from the stored event history.

The IdentityStore stores public and verifiable identity information only.

Private keys and other secret cryptographic material **MUST NOT** be stored in the `IdentityStore`.

The logical event history is append-only. Physical storage mechanisms **MAY** use compaction or other optimizations as long as the information required to reconstruct and verify the identity state is preserved.

---

#### 14.3 Event Ingestion

```text
            EVENT
              │
              ▼
        Identification 
              │
              ▼
       Structural check
              │
              ▼
       Signature check
              │
        ┌─────┴─────┐
        ▼           ▼
    INVALID        VALID
                    │
                    ▼
            Resolve references
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
    MISSING      CONFLICT      READY
       │            │            │
       ▼            ▼            ▼
  INCOMPLETE     BLOCKED     Apply rules
                                 │
                   ┌─────────────┼─────────────┐
                   ▼             ▼             ▼
                ACTIVE        INACTIVE      REVOKED
```

---

#### 14.4 Graph Reconstruction

The `IdentityStore` stores events and reconstructs the graph by determining the state based on **successions**, **dependencies**, and **revocations**.

---

#### 14.5 State Reconstruction

The **global state is reconstructed from the state of the graph**. If the graph contains **no incomplete elements** and **no blocking** `CONFLICT`, the global state is `STABLE`.

---

### 15. Synchronization

#### 15.1 Multi-machine State

The same `Identity` **MAY** be represented and updated independently on multiple machines.

---

#### 15.2 Out-of-order Events

The reception order **does not** define the logical order of `Events`. The logical order is determined by the relationship between the `Events`.

---

#### 15.3 Duplicates

An `Event` whose `Event ID` is already known is treated as a duplicate and **MUST NOT** create a second journal entry.

---

#### 15.4 Missing Events

A missing dependency results in the statuses `INCOMPLETE` and `BLOCKED` for the items that depend on it.

---

#### 15.5 Concurrent Changes

Two concurrent changes create a `CONFLICT` that **MUST** be resolved by the protocol.

---

### 16. Conflict Resolution

#### 16.1 Conflict Identification

```text
If:
ROOT_A
 ├── ROOT_B (valid)
 └── ROOT_C (valid)

→ CONFLICT
```


---

#### 16.2 Resolution Authority

*To be determined.*

---

#### 16.3 Resolution Event

A `CONFLICT` is derived from the Event Graph.

A `ConflictResolution` Event is created when an authorized resolution decision is made.

#### 16.4 Branch Selection

The branch selection **MUST not** be automatic. It **MUST** require user action.

---

### 17. Trust

#### 17.1 TrustManager

The `TrustManager` is the mechanism that determines whether an `Identity` or a `Root` is recognized as trustworthy.
A cryptographic validity does not imply a trust situation.

---
#### 17.2 TrustRecord

`TrustRecord` identifies the `Root` that we currently consider trustworthy for an `Identity`.

---

#### 17.3 TrustBootstrap

`TrustBootstrap` is the mechanism by which a trust relationship is initially established between an `Identity` and a `Root`.

---

#### 17.4 PRECONFIGURED

The `Identity` is already known and configured.

---

#### 17.5 FINGERPRINT

The fingerprint is transmitted over a **separate**, **secure channel**.

---

#### 17.6 TOFU

On first observation, the `Root` is stored as the trust anchor according to the local TOFU policy.

A later unexpected `Root` change **MUST** be reported as a trust state change and **MUST NOT** be silently accepted.

---

### 18. Security Considerations

- Compromised root private key
- Non-secret identity ID
- Event immutability
- Signature validation
- Nonce uniqueness
- Conflict handling
- Trust bootstrap risks
- TOFU first-contact risk
- Out-of-band fingerprint trust requirement

---

### 19. Invariants

- Events are immutable.
- Every event has an `Event ID`.
- Events belong to exactly one `Identity ID`.
- Reception order does not define logical order.
- `INVALID` events cannot become `VALID`.
- `INCOMPLETE` events may become `VALID`.
- A conflict **MUST NOT** be silently resolved.
- Conflicting branches **MUST NOT** be deleted.
- Dependents of unresolved conflicts are `BLOCKED`.
- ConflictResolution is itself an authenticated event.
- Re-evaluation propagates to affected dependents.
- Causal dependencies **MUST NOT** form cycles.
- Trust is not inferred solely from cryptographic validity.
- Private keys **MUST NOT** be stored in `IdentityStore`.
- The protocol requires a **verifiable cryptographic signature** and specifies the algorithm used; the cryptographic suites and their parameters are defined in a dedicated cryptographic specification.
- The recovery capability **MUST** remain usable when the root it is intended to replace is compromised.
- Authorization state is monotonic with respect to quorum satisfaction: once an operation has satisfied its required authorization threshold, a later revocation **cannot** reduce the already satisfied authorization quorum.

---

### 20. Open Questions

#### OQ-001

Initial RootRecord authority ?

PROPOSED RESOLUTION:

The initial RootRecord is self-authenticated by the private key corresponding to the Root public key contained in the RootRecord.

Trust in the Root is established separately through TrustBootstrap and TrustManager.

---

#### OQ-002

IdentityComponent lifecycle and authorization model ?

PROPOSED RESOLUTION:

`IdentityComponent` is an autonomous Event in the Identity Journal.

A valid `IdentityComponent` Event establishes the existence and cryptographic identity of an operational Component.

A `KeyDelegation` separately grants operational authority to the Component.

The `Issuer` of an `IdentityComponent` is a Root authorized to create Components.

A Component created by a historical Root remains historically valid, but its current operational effect is determined by the protocol's applicability rules.

The exact authorization rules governing Component creation remain to be defined.

---

#### OQ-003

ConflictResolution authority ?

PROPOSED RESOLUTION:

The Root is the primary authority of an Identity.

A dedicated Recovery Component MAY be granted explicit recovery permissions such as `ROOT_SUCCESSION` and `CONFLICT_RESOLUTION`.

A Recovery authority MUST be established before the failure or compromise of the Root it is intended to recover.

The exact rules governing the protection, revocation, precedence, and authority of Recovery Components remain to be defined.

---

#### OQ-004

How should a causal dependency cycle be classified ?

---

#### OQ-005 

Recovery Key Revocation Authority ?

PROPOSED RESOLUTION:

RECOVERY_MANAGEMENT
+
threshold 2-of-N

---

#### OQ-006 

Recovery Authority Multiplicity ?

PROPOSED RESOLUTION:

Recovery Components are independent cryptographic Components.
Their permissions are explicitly delegated and should not be implicitly shared or inherited.

A dedicated recovery-management permission may be used to revoke Recovery Components without relying on the Root.

Recovery Components indépendants
+
permissions explicitement séparées
+
politiques de seuil par opération

---

#### OQ-007

Threshold Policy ?

---

#### OQ-008

Recovery Authority Set Management ?
How is the Recovery Authority Set initialized, modified, and protected? Which authorities are eligible to add or remove Recovery Components, and what authorization threshold is required ?

PROPOSED RESOLUTION:

1. The initial Recovery Authority Set is established during identity bootstrap because no Recovery Authority exists yet.

2. Bootstrap must establish enough Recovery Authorities to satisfy all mandatory Recovery policies.

3. After bootstrap, Root cannot unilaterally modify the Recovery Authority Set.

4. Add/remove operations affecting the Recovery Authority Set require RECOVERY_MANAGEMENT authorization according to the applicable threshold policy.

5. A Set modification must not leave the identity unable to satisfy mandatory Recovery policies.

---

#### OQ-009

How should threshold-based authorization be represented in the event journal, and how are individual Authorization Events associated with the operation they authorize ?

PROPOSED RESOLUTION:

Threshold-based authorization is represented using independent Authorization Events.

Each Authorization Event:
- is signed by one authorized Component;
- references exactly one Operation ID;
- is independently verifiable;
- contributes at most once to the authorization threshold of that
  operation.

The authorization threshold is evaluated over the set of distinct, eligible authorities that have issued valid Authorization Events for the operation.

Authorization Events remain immutable and are not modified or marked as consumed when their authorization is used.

---

#### OQ-010

How should an Authorization Event identify the authority set and authorization policy applicable to the operation at the time the authorization is issued ?

PROPOSED RESOLUTION:

Each threshold-based operation is bound to an immutable authorization context.

The authorization context identifies the Recovery Authority Set and the authorization policy applicable to the operation.

Authorization Events must be evaluated against the authorization context of the operation and cannot implicitly adopt later changes to the authority set or authorization policy.

Changes to the Recovery Authority Set or its authorization policies therefore affect future operations unless explicitly defined otherwise by the protocol.

---

#### OQ-011

How does the revocation of an authority affect previously issued Authorization Events, particularly when the authorized operation has not yet reached its required threshold?

How are concurrent authorization and revocation events handled?

PROPOSED RESOLUTION:

An Authorization Event is historically valid if its issuer was authorized to perform the corresponding operation within the applicable authorization context when the event was issued.

A later revocation does not invalidate an Authorization Event historically.

However, until an operation has satisfied its required authorization threshold, a revoked authority must no longer be able to provide a new authorization contribution to that operation.

Once the required authorization threshold has been satisfied, the authorization quorum is not retroactively invalidated by a later revocation.

Concurrent authorization and revocation events must be evaluated using the event graph, authorization context, and causal dependencies, not Created At alone.

---

#### OQ-012

Who may create an OperationRequest, and are any operation types restricted to specific proposers?

PROPOSED RESOLUTION:



---

#### OQ-013

How is the immutable authorization context of an OperationRequest anchored to a specific Recovery Authority Set state and authorization policy state?

PROPOSED RESOLUTION:

An OperationRequest references an immutable Authority Context ID.

The Authority Context ID is derived from the canonical representation of the complete authority state relevant to protected Recovery operations.

When a context-modifying OperationRequest becomes READY, its protocol-defined Effect is deterministically applied to the referenced authority context.

IdentityStore reconstructs the resulting authority state and computes a new Authority Context ID from its canonical representation.

No additional state-transition event is required if the resulting state is fully and deterministically derivable from the READY OperationRequest and its dependencies.

---

#### OQ-014

How is the authorization policy applicable to an operation determined and verified, and how is an invalid or unauthorized policy declaration handled?

PROPOSED RESOLUTION:

The authorization policy applicable to an OperationRequest is not chosen by the operation creator.

It is deterministically resolved from:
- Operation Type + referenced Authority Context

An OperationRequest does not redefine its required permission or authorization threshold.

The referenced Authority Context must itself be valid and applicable to the operation.

Historical authority contexts cannot be reused to bypass later authority or policy changes.

Concurrent operations legitimately derived from the same applicable context may create competing context branches and are handled through the normal conflict-resolution mechanism.

---

### 21. Future Extensions

Possible future extensions of the Kryptos identity protocol include:

- additional trust bootstrap mechanisms;
- additional recovery mechanisms;
- threshold or multi-party recovery;
- additional delegation models;
- additional identity event types;
- additional conflict resolution mechanisms;
- distributed or remote identity stores;
- protocol evolution for post-quantum cryptographic algorithms.

These extensions are not part of the current specification.

---
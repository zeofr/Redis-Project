# Redis NoSQL Operations Manual
## Complete Guide to Redis CLI Commands

---

## Table of Contents
1. [Getting Started](#getting-started)
2. [String Operations](#1-string-operations)
3. [Hash Operations (CRUD)](#2-hash-operations-crud)
4. [List Operations](#3-list-operations)
5. [Set Operations](#4-set-operations)
6. [Sorted Set Operations](#5-sorted-set-operations)
7. [Search & Filter Operations](#6-search--filter-operations)
8. [Expiration & TTL](#7-expiration--ttl)
9. [Transactions](#8-transactions)
10. [Key Management](#9-key-management)

---

## Getting Started

### Connect to Redis CLI
```bash
redis-cli
```

### Clear the database (optional - be careful!)
```bash
FLUSHDB
```

### Test connection
```bash
PING
# Expected output: PONG
```

---

## 1. STRING OPERATIONS
**Description**: Basic key-value pairs. Simplest data structure in Redis.

### Set a string value
```bash
SET user:1000:name "John Doe"
SET user:1000:email "john@example.com"
SET user:1000:age 28
```

### Get a string value
```bash
GET user:1000:name
# Output: "John Doe"

GET user:1000:age
# Output: "28"
```

### Increment a numeric value
```bash
INCR user:1000:age
# Output: (integer) 29

GET user:1000:age
# Output: "29"
```

### Decrement a value
```bash
DECR user:1000:age
# Output: (integer) 28
```

### Set multiple values at once
```bash
MSET config:timeout 30 config:retries 3 config:enabled true
```

### Get multiple values at once
```bash
MGET config:timeout config:retries config:enabled
# Output:
# 1) "30"
# 2) "3"
# 3) "true"
```

### Append to a string
```bash
SET greeting "Hello"
APPEND greeting " World"
GET greeting
# Output: "Hello World"
```

---

## 2. HASH OPERATIONS (CRUD)
**Description**: Hash maps - similar to documents in MongoDB. Perfect for representing objects with multiple fields.

### CREATE - Insert hash documents

#### Create a single user with multiple fields
```bash
HSET user:1 name "Alice Johnson" email "alice@example.com" age 25 city "New York" role "developer"
```

#### Create more users
```bash
HSET user:2 name "Bob Smith" email "bob@example.com" age 32 city "San Francisco" role "designer"
HSET user:3 name "Carol White" email "carol@example.com" age 28 city "New York" role "developer"
HSET user:4 name "David Brown" email "david@example.com" age 35 city "Boston" role "manager"
```

### READ - Retrieve hash documents

#### Get all fields of a hash
```bash
HGETALL user:1
# Output:
# 1) "name"
# 2) "Alice Johnson"
# 3) "email"
# 4) "alice@example.com"
# 5) "age"
# 6) "25"
# ...
```

#### Get a specific field
```bash
HGET user:1 name
# Output: "Alice Johnson"

HGET user:2 city
# Output: "San Francisco"
```

#### Get multiple fields
```bash
HMGET user:1 name email age
# Output:
# 1) "Alice Johnson"
# 2) "alice@example.com"
# 3) "25"
```

#### Check if field exists
```bash
HEXISTS user:1 name
# Output: (integer) 1 (exists)

HEXISTS user:1 salary
# Output: (integer) 0 (doesn't exist)
```

#### Get all field names
```bash
HKEYS user:1
# Output: 1) "name" 2) "email" 3) "age" 4) "city" 5) "role"
```

#### Get all values
```bash
HVALS user:1
# Output: 1) "Alice Johnson" 2) "alice@example.com" 3) "25" 4) "New York" 5) "developer"
```

#### Get number of fields
```bash
HLEN user:1
# Output: (integer) 5
```

### UPDATE - Modify hash documents

#### Update a single field
```bash
HSET user:1 age 26
```

#### Add a new field
```bash
HSET user:1 department "Engineering"
```

#### Increment a numeric field
```bash
HINCRBY user:1 age 1
# Increments age by 1
```

#### Update multiple fields at once
```bash
HSET user:2 age 33 city "Los Angeles" department "Design"
```

### DELETE - Remove hash fields or entire documents

#### Delete a specific field
```bash
HDEL user:2 city
# Output: (integer) 1 (1 field deleted)
```

#### Delete multiple fields
```bash
HDEL user:3 city role
# Output: (integer) 2 (2 fields deleted)
```

#### Delete entire hash (document)
```bash
DEL user:4
# Output: (integer) 1 (1 key deleted)
```

---

## 3. LIST OPERATIONS
**Description**: Ordered collections - can be used as stacks, queues, or simple arrays.

### Add elements to list

#### Add to the right (end) of list
```bash
RPUSH tasks:pending "Task 1: Design database schema"
RPUSH tasks:pending "Task 2: Implement API"
RPUSH tasks:pending "Task 3: Write tests"
```

#### Add to the left (beginning) of list
```bash
LPUSH tasks:pending "Task 0: Setup project"
```

#### Add multiple elements at once
```bash
RPUSH notifications "Email sent" "SMS delivered" "Push notification sent"
```

### Retrieve elements from list

#### Get all elements (0 to -1 means start to end)
```bash
LRANGE tasks:pending 0 -1
# Output:
# 1) "Task 0: Setup project"
# 2) "Task 1: Design database schema"
# 3) "Task 2: Implement API"
# 4) "Task 3: Write tests"
```

#### Get first 2 elements
```bash
LRANGE tasks:pending 0 1
```

#### Get element at specific index
```bash
LINDEX tasks:pending 0
# Output: "Task 0: Setup project"
```

#### Get list length
```bash
LLEN tasks:pending
# Output: (integer) 4
```

### Remove elements from list

#### Remove and return first element (left pop)
```bash
LPOP tasks:pending
# Output: "Task 0: Setup project"
```

#### Remove and return last element (right pop)
```bash
RPOP tasks:pending
# Output: "Task 3: Write tests"
```

### Update list elements

#### Set element at specific index
```bash
LSET tasks:pending 0 "Task 1: Design schema (UPDATED)"
```

#### Remove elements by value
```bash
LREM tasks:pending 1 "Task 2: Implement API"
# Removes 1 occurrence of the value
```

#### Trim list to keep only specific range
```bash
LTRIM tasks:pending 0 2
# Keeps only first 3 elements
```

---

## 4. SET OPERATIONS
**Description**: Unordered collections of unique elements. Great for tags, categories, memberships.

### Add members to sets
```bash
SADD skills:python "Alice" "Bob" "Carol"
SADD skills:javascript "Bob" "Carol" "David"
SADD skills:java "Alice" "David"
SADD skills:docker "Alice" "Eve"
```

### View set members
```bash
SMEMBERS skills:python
# Output:
# 1) "Alice"
# 2) "Bob"
# 3) "Carol"
```

### Check membership
```bash
SISMEMBER skills:python "Alice"
# Output: (integer) 1 (is a member)

SISMEMBER skills:python "David"
# Output: (integer) 0 (not a member)
```

### Get set size
```bash
SCARD skills:python
# Output: (integer) 3
```

### Set operations (intersections, unions, differences)

#### Intersection (AND) - Members in BOTH sets
```bash
SINTER skills:python skills:javascript
# Output: 1) "Bob" 2) "Carol"
# (People who know both Python AND JavaScript)
```

#### Union (OR) - Members in EITHER set
```bash
SUNION skills:python skills:java
# Output: 1) "Alice" 2) "Bob" 3) "Carol" 4) "David"
# (People who know Python OR Java)
```

#### Difference - Members in first set but NOT in second
```bash
SDIFF skills:python skills:javascript
# Output: 1) "Alice"
# (People who know Python but NOT JavaScript)
```

#### Store result of set operation
```bash
SINTERSTORE skills:fullstack skills:python skills:javascript
# Creates new set with the intersection
```

### Remove members
```bash
SREM skills:python "Bob"
# Output: (integer) 1 (1 member removed)
```

### Pop random member
```bash
SPOP skills:python
# Returns and removes a random member
```

---

## 5. SORTED SET OPERATIONS
**Description**: Sets where each member has a score for sorting. Perfect for leaderboards, rankings, priority queues.

### Add members with scores
```bash
ZADD leaderboard:game1 1500 "Alice"
ZADD leaderboard:game1 2300 "Bob"
ZADD leaderboard:game1 1800 "Carol"
ZADD leaderboard:game1 2100 "David"
ZADD leaderboard:game1 1950 "Eve"
```

#### Add multiple members at once
```bash
ZADD leaderboard:game2 1000 "Frank" 1200 "Grace" 900 "Henry"
```

### Retrieve members (sorted by score)

#### Get all members with scores (ascending order)
```bash
ZRANGE leaderboard:game1 0 -1 WITHSCORES
# Output:
# 1) "Alice"
# 2) "1500"
# 3) "Carol"
# 4) "1800"
# 5) "Eve"
# 6) "1950"
# 7) "David"
# 8) "2100"
# 9) "Bob"
# 10) "2300"
```

#### Get members in descending order (highest scores first)
```bash
ZREVRANGE leaderboard:game1 0 -1 WITHSCORES
# Output:
# 1) "Bob"
# 2) "2300"
# 3) "David"
# 4) "2100"
# ...
```

#### Get top 3 players
```bash
ZREVRANGE leaderboard:game1 0 2 WITHSCORES
```

### Range queries by score

#### Get members with score between 1800 and 2200
```bash
ZRANGEBYSCORE leaderboard:game1 1800 2200 WITHSCORES
# Output:
# 1) "Carol"
# 2) "1800"
# 3) "Eve"
# 4) "1950"
# 5) "David"
# 6) "2100"
```

#### Get members with score above 2000
```bash
ZRANGEBYSCORE leaderboard:game1 2000 +inf WITHSCORES
```

### Get member information

#### Get score of a specific member
```bash
ZSCORE leaderboard:game1 "Alice"
# Output: "1500"
```

#### Get rank (position) of member (0-indexed, ascending)
```bash
ZRANK leaderboard:game1 "Carol"
# Output: (integer) 2 (3rd position from bottom)
```

#### Get reverse rank (position from top)
```bash
ZREVRANK leaderboard:game1 "Carol"
# Output: (integer) 2 (3rd position from top)
```

#### Count members in score range
```bash
ZCOUNT leaderboard:game1 1800 2200
# Output: (integer) 3
```

### Update scores

#### Increment score
```bash
ZINCRBY leaderboard:game1 300 "Alice"
# Adds 300 to Alice's score
# Output: "1800"
```

#### Decrement score (use negative number)
```bash
ZINCRBY leaderboard:game1 -100 "Bob"
# Subtracts 100 from Bob's score
```

### Remove members
```bash
ZREM leaderboard:game1 "David"
# Output: (integer) 1 (1 member removed)
```

#### Remove members by rank range
```bash
ZREMRANGEBYRANK leaderboard:game1 0 0
# Removes lowest scoring member
```

#### Remove members by score range
```bash
ZREMRANGEBYSCORE leaderboard:game1 0 1000
# Removes all members with score between 0-1000
```

### Get sorted set size
```bash
ZCARD leaderboard:game1
# Output: (integer) 4
```

---

## 6. SEARCH & FILTER OPERATIONS
**Description**: Finding and filtering keys using patterns.

### Pattern matching with KEYS (⚠️ Use SCAN in production)
```bash
KEYS user:*
# Output: 1) "user:1" 2) "user:2" 3) "user:3"

KEYS *:pending
# Output: 1) "tasks:pending"

KEYS user:?
# Output: 1) "user:1" 2) "user:2" 3) "user:3"
```

**Note**: KEYS blocks the server. Use SCAN in production!

### Pattern matching with SCAN (recommended)
```bash
SCAN 0 MATCH user:* COUNT 100
# Output:
# 1) "0" (cursor)
# 2) 1) "user:1"
#    2) "user:2"
#    3) "user:3"
```

### Find all keys of a specific type
```bash
# First, find all keys
KEYS *

# Then check type of each
TYPE user:1
# Output: hash

TYPE tasks:pending
# Output: list

TYPE skills:python
# Output: set
```

### Search within hash values (requires iteration)
```bash
# Get all users
KEYS user:*

# For each user, check fields
HGETALL user:1
HGETALL user:2
HGETALL user:3

# Check specific field
HGET user:1 role
HGET user:2 role
```

**Note**: For complex queries, consider using:
- **RediSearch module** for full-text search
- **RedisJSON module** for JSON path queries
- Client-side filtering (as shown in Python script)

---

## 7. EXPIRATION & TTL
**Description**: Automatic key expiration - useful for sessions, caches, temporary data.

### Set key with expiration on creation
```bash
SETEX session:user123 300 "active"
# Key expires in 300 seconds (5 minutes)
```

### Set expiration on existing key
```bash
SET temp:data "temporary value"
EXPIRE temp:data 60
# Expires in 60 seconds
```

### Check time-to-live (TTL)
```bash
TTL session:user123
# Output: (integer) 295 (seconds remaining)
```

### Set expiration with milliseconds
```bash
PSETEX temp:fast 5000 "expires in 5 seconds"
# Expires in 5000 milliseconds

PTTL temp:fast
# Output: (integer) 4850 (milliseconds remaining)
```

### Set expiration at specific timestamp
```bash
EXPIREAT mykey 1735689600
# Expires at Unix timestamp
```

### Remove expiration (make key persistent)
```bash
PERSIST session:user123
# Output: (integer) 1 (expiration removed)
```

### Check if key will expire
```bash
TTL mykey
# Output:
# -1 = key exists but no expiration
# -2 = key doesn't exist
# positive number = seconds until expiration
```

---

## 8. TRANSACTIONS
**Description**: Execute multiple commands atomically - all succeed or all fail.

### Basic transaction
```bash
MULTI
SET account:1 100
SET account:2 200
EXEC
```

### Transfer funds atomically
```bash
# Setup
HSET user:1 points 500
HSET user:2 points 300

# Transaction - transfer 100 points from user:1 to user:2
MULTI
HINCRBY user:1 points -100
HINCRBY user:2 points 100
EXEC

# Verify
HGET user:1 points
# Output: "400"
HGET user:2 points
# Output: "400"
```

### Discard transaction
```bash
MULTI
SET key1 "value1"
SET key2 "value2"
DISCARD
# Commands are discarded, not executed
```

### Watch keys for optimistic locking
```bash
WATCH account:balance
# ... check balance ...
MULTI
DECRBY account:balance 100
EXEC
# EXEC fails if account:balance was modified after WATCH
```

---

## 9. KEY MANAGEMENT
**Description**: Operations to manage, inspect, and monitor keys.

### Check if key exists
```bash
EXISTS user:1
# Output: (integer) 1 (exists)

EXISTS user:999
# Output: (integer) 0 (doesn't exist)
```

### Check multiple keys at once
```bash
EXISTS user:1 user:2 user:999
# Output: (integer) 2 (2 out of 3 exist)
```

### Get key type
```bash
TYPE user:1
# Output: hash

TYPE tasks:pending
# Output: list

TYPE skills:python
# Output: set
```

### Delete keys
```bash
DEL user:4
# Output: (integer) 1 (1 key deleted)

DEL key1 key2 key3
# Delete multiple keys at once
```

### Rename key
```bash
RENAME oldkey newkey
```

### Rename only if new key doesn't exist
```bash
RENAMENX oldkey newkey
# Output: (integer) 1 (success)
# Output: (integer) 0 (newkey already exists)
```

### Get total number of keys
```bash
DBSIZE
# Output: (integer) 15
```

### Get random key
```bash
RANDOMKEY
# Output: "user:2"
```

### Database management

#### Select database (0-15 by default)
```bash
SELECT 1
# Switch to database 1
```

#### Clear current database
```bash
FLUSHDB
# ⚠️ Deletes all keys in current database
```

#### Clear all databases
```bash
FLUSHALL
# ⚠️ Deletes all keys in ALL databases
```

### Server information
```bash
INFO
# Shows detailed server statistics

INFO keyspace
# Shows info about databases and key counts

DBSIZE
# Returns number of keys in current database

LASTSAVE
# Unix timestamp of last DB save
```

### Monitor commands in real-time
```bash
MONITOR
# Shows all commands being executed (for debugging)
# Press Ctrl+C to stop
```

---

## Quick Reference Commands

### String Commands
```bash
SET key value          # Set string value
GET key               # Get string value
INCR key              # Increment by 1
DECR key              # Decrement by 1
APPEND key value      # Append to string
```

### Hash Commands
```bash
HSET key field value         # Set hash field
HGET key field               # Get hash field
HGETALL key                  # Get all fields
HDEL key field               # Delete field
HEXISTS key field            # Check if field exists
```

### List Commands
```bash
LPUSH key value       # Push to left
RPUSH key value       # Push to right
LPOP key              # Pop from left
RPOP key              # Pop from right
LRANGE key start stop # Get range
LLEN key              # Get length
```

### Set Commands
```bash
SADD key member       # Add member
SMEMBERS key          # Get all members
SISMEMBER key member  # Check membership
SREM key member       # Remove member
SINTER key1 key2      # Intersection
SUNION key1 key2      # Union
SDIFF key1 key2       # Difference
```

### Sorted Set Commands
```bash
ZADD key score member        # Add member with score
ZRANGE key start stop        # Get range (ascending)
ZREVRANGE key start stop     # Get range (descending)
ZSCORE key member            # Get score
ZRANK key member             # Get rank
ZINCRBY key increment member # Increment score
```

### Key Management
```bash
EXISTS key            # Check if exists
TYPE key              # Get type
DEL key               # Delete key
KEYS pattern          # Find keys (use SCAN instead)
SCAN cursor MATCH pattern  # Iterate keys
TTL key               # Time to live
EXPIRE key seconds    # Set expiration
```

---

## Practice Exercise

Try creating a complete user management system:

```bash
# 1. Create users
HSET user:alice name "Alice" age 25 email "alice@example.com"
HSET user:bob name "Bob" age 30 email "bob@example.com"

# 2. Add them to skill sets
SADD skills:python alice bob
SADD skills:java alice

# 3. Create a leaderboard
ZADD scores:project1 95 alice
ZADD scores:project1 88 bob

# 4. Create a task list
RPUSH tasks:alice "Task 1" "Task 2" "Task 3"

# 5. Set session with expiration
SETEX session:alice 3600 "logged_in"

# 6. Check everything
HGETALL user:alice
SMEMBERS skills:python
ZREVRANGE scores:project1 0 -1 WITHSCORES
LRANGE tasks:alice 0 -1
TTL session:alice
```

---

## Tips for Your Presentation

1. **Start Simple**: Begin with STRING operations, then move to complex types
2. **Show CRUD**: Demonstrate Create, Read, Update, Delete for hashes
3. **Real Examples**: Use realistic data (users, products, tasks)
4. **Compare to SQL**: Mention how Redis differs from relational databases
5. **Performance**: Highlight Redis speed and in-memory nature
6. **Use Cases**: Mention caching, sessions, leaderboards, queues

---

## Additional Resources

- Redis Official Documentation: https://redis.io/docs/
- Redis Commands Reference: https://redis.io/commands/
- Try Redis Online: https://try.redis.io/

---

**End of Manual**

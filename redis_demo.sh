#!/bin/bash
# Redis NoSQL Operations Demo - CLI Commands
# Copy and paste these commands into redis-cli

# ============================================================
# SETUP - Clear database and start fresh
# ============================================================
echo "Clearing database..."
redis-cli FLUSHDB
redis-cli PING

# ============================================================
# 1. STRING OPERATIONS
# ============================================================
echo ""
echo "=== 1. STRING OPERATIONS ==="

# Set string values
redis-cli SET user:1000:name "John Doe"
redis-cli SET user:1000:email "john@example.com"
redis-cli SET user:1000:age 28

# Get string values
redis-cli GET user:1000:name
redis-cli GET user:1000:age

# Increment
redis-cli INCR user:1000:age
redis-cli GET user:1000:age

# Multiple set/get
redis-cli MSET config:timeout 30 config:retries 3
redis-cli MGET config:timeout config:retries

# ============================================================
# 2. HASH OPERATIONS (CRUD)
# ============================================================
echo ""
echo "=== 2. HASH OPERATIONS (CRUD) ==="

# CREATE - Insert documents
redis-cli HSET user:1 name "Alice Johnson" email "alice@example.com" age 25 city "New York" role "developer"
redis-cli HSET user:2 name "Bob Smith" email "bob@example.com" age 32 city "San Francisco" role "designer"
redis-cli HSET user:3 name "Carol White" email "carol@example.com" age 28 city "New York" role "developer"
redis-cli HSET user:4 name "David Brown" email "david@example.com" age 35 city "Boston" role "manager"

# READ - Retrieve documents
redis-cli HGETALL user:1
redis-cli HGET user:2 name
redis-cli HMGET user:1 name email age
redis-cli HEXISTS user:1 name
redis-cli HKEYS user:1
redis-cli HLEN user:1

# UPDATE - Modify documents
redis-cli HSET user:1 age 26
redis-cli HSET user:1 department "Engineering"
redis-cli HINCRBY user:1 age 1
redis-cli HGETALL user:1

# DELETE - Remove fields or documents
redis-cli HDEL user:2 city
redis-cli HGETALL user:2
redis-cli DEL user:4

# ============================================================
# 3. LIST OPERATIONS
# ============================================================
echo ""
echo "=== 3. LIST OPERATIONS ==="

# Add to list
redis-cli RPUSH tasks:pending "Task 1: Design database schema"
redis-cli RPUSH tasks:pending "Task 2: Implement API"
redis-cli RPUSH tasks:pending "Task 3: Write tests"
redis-cli LPUSH tasks:pending "Task 0: Setup project"

# View list
redis-cli LRANGE tasks:pending 0 -1
redis-cli LLEN tasks:pending
redis-cli LINDEX tasks:pending 0

# Pop from list
redis-cli LPOP tasks:pending
redis-cli LRANGE tasks:pending 0 -1

# ============================================================
# 4. SET OPERATIONS
# ============================================================
echo ""
echo "=== 4. SET OPERATIONS ==="

# Add to sets
redis-cli SADD skills:python "Alice" "Bob" "Carol"
redis-cli SADD skills:javascript "Bob" "Carol" "David"
redis-cli SADD skills:java "Alice" "David"

# View sets
redis-cli SMEMBERS skills:python
redis-cli SMEMBERS skills:javascript
redis-cli SCARD skills:python

# Set operations
redis-cli SINTER skills:python skills:javascript
redis-cli SUNION skills:python skills:java
redis-cli SDIFF skills:python skills:javascript

# Check membership
redis-cli SISMEMBER skills:python "Alice"
redis-cli SISMEMBER skills:python "David"

# ============================================================
# 5. SORTED SET OPERATIONS
# ============================================================
echo ""
echo "=== 5. SORTED SET OPERATIONS ==="

# Add with scores
redis-cli ZADD leaderboard:game1 1500 "Alice"
redis-cli ZADD leaderboard:game1 2300 "Bob"
redis-cli ZADD leaderboard:game1 1800 "Carol"
redis-cli ZADD leaderboard:game1 2100 "David"
redis-cli ZADD leaderboard:game1 1950 "Eve"

# View sorted (ascending)
redis-cli ZRANGE leaderboard:game1 0 -1 WITHSCORES

# View sorted (descending - leaderboard style)
redis-cli ZREVRANGE leaderboard:game1 0 -1 WITHSCORES

# Get top 3
redis-cli ZREVRANGE leaderboard:game1 0 2 WITHSCORES

# Range by score
redis-cli ZRANGEBYSCORE leaderboard:game1 1800 2200 WITHSCORES

# Get score
redis-cli ZSCORE leaderboard:game1 "Alice"

# Get rank
redis-cli ZRANK leaderboard:game1 "Carol"
redis-cli ZREVRANK leaderboard:game1 "Carol"

# Increment score
redis-cli ZINCRBY leaderboard:game1 300 "Alice"
redis-cli ZSCORE leaderboard:game1 "Alice"

# Count in range
redis-cli ZCOUNT leaderboard:game1 1800 2200

# ============================================================
# 6. SEARCH & FILTER OPERATIONS
# ============================================================
echo ""
echo "=== 6. SEARCH & FILTER ==="

# Pattern matching
redis-cli KEYS user:*
redis-cli KEYS *:pending
redis-cli SCAN 0 MATCH user:* COUNT 100

# Check types
redis-cli TYPE user:1
redis-cli TYPE tasks:pending
redis-cli TYPE skills:python

# ============================================================
# 7. EXPIRATION & TTL
# ============================================================
echo ""
echo "=== 7. EXPIRATION & TTL ==="

# Set with expiration
redis-cli SETEX session:user123 300 "active"
redis-cli TTL session:user123

# Set expiration on existing key
redis-cli SET temp:data "temporary value"
redis-cli EXPIRE temp:data 60
redis-cli TTL temp:data

# Remove expiration
redis-cli PERSIST temp:data
redis-cli TTL temp:data

# ============================================================
# 8. TRANSACTIONS
# ============================================================
echo ""
echo "=== 8. TRANSACTIONS ==="

# Setup
redis-cli HSET account:1 balance 500
redis-cli HSET account:2 balance 300

# Transaction - transfer funds
redis-cli MULTI
redis-cli HINCRBY account:1 balance -100
redis-cli HINCRBY account:2 balance 100
redis-cli EXEC

# Verify
redis-cli HGET account:1 balance
redis-cli HGET account:2 balance

# ============================================================
# 9. KEY MANAGEMENT & STATISTICS
# ============================================================
echo ""
echo "=== 9. KEY MANAGEMENT ==="

# Check existence
redis-cli EXISTS user:1
redis-cli EXISTS user:999

# Get type
redis-cli TYPE user:1
redis-cli TYPE leaderboard:game1

# Database size
redis-cli DBSIZE

# Get random key
redis-cli RANDOMKEY

# Server info
redis-cli INFO keyspace

echo ""
echo "=== ALL OPERATIONS COMPLETED ==="
echo "Use 'redis-cli KEYS *' to see all keys created"
echo "Use 'redis-cli FLUSHDB' to clear everything"

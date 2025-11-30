import redis
import json
from datetime import datetime

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def clear_demo_data():
    """Clear all demo data"""
    print("\n" + "="*60)
    print("CLEARING PREVIOUS DEMO DATA")
    print("="*60)
    r.flushdb()
    print("✓ Database cleared")

def demo_string_operations():
    """Basic String operations (Key-Value pairs)"""
    print("\n" + "="*60)
    print("1. STRING OPERATIONS (Key-Value Store)")
    print("="*60)
    
    # SET operations
    r.set("user:1000:name", "John Doe")
    print("  CLI: SET user:1000:name \"John Doe\"")
    r.set("user:1000:email", "john@example.com")
    print("  CLI: SET user:1000:email \"john@example.com\"")
    r.set("user:1000:age", 28)
    print("  CLI: SET user:1000:age 28")
    
    print("\n✓ Created string keys:")
    print(f"  user:1000:name = {r.get('user:1000:name')}")
    print("  CLI: GET user:1000:name")
    print(f"  user:1000:email = {r.get('user:1000:email')}")
    print(f"  user:1000:age = {r.get('user:1000:age')}")
    
    # Increment operation
    r.incr("user:1000:age")
    print(f"\n✓ After increment: user:1000:age = {r.get('user:1000:age')}")
    print("  CLI: INCR user:1000:age")
    
    # Multiple set/get
    r.mset({"config:timeout": "30", "config:retries": "3"})
    print(f"\n✓ Multiple set: {r.mget(['config:timeout', 'config:retries'])}")
    print("  CLI: MSET config:timeout 30 config:retries 3")
    print("  CLI: MGET config:timeout config:retries")

def demo_hash_operations():
    """Hash operations (Similar to documents/objects)"""
    print("\n" + "="*60)
    print("2. HASH OPERATIONS (Document Store - Like MongoDB Documents)")
    print("="*60)
    
    # Create user documents
    users = [
        {"id": "1", "name": "Alice Johnson", "email": "alice@example.com", 
         "age": "25", "city": "New York", "role": "developer"},
        {"id": "2", "name": "Bob Smith", "email": "bob@example.com", 
         "age": "32", "city": "San Francisco", "role": "designer"},
        {"id": "3", "name": "Carol White", "email": "carol@example.com", 
         "age": "28", "city": "New York", "role": "developer"},
        {"id": "4", "name": "David Brown", "email": "david@example.com", 
         "age": "35", "city": "Boston", "role": "manager"},
    ]
    
    # CREATE - Insert documents
    print("\n--- CREATE Operations ---")
    for user in users:
        user_id = user.pop("id")
        r.hset(f"user:{user_id}", mapping=user)
        print(f"✓ Created user:{user_id}")
    print("  CLI: HSET user:1 name \"Alice Johnson\" email \"alice@example.com\" age 25 city \"New York\" role developer")
    
    # READ - Retrieve documents
    print("\n--- READ Operations ---")
    user1 = r.hgetall("user:1")
    print(f"✓ Get user:1 -> {user1}")
    print("  CLI: HGETALL user:1")
    
    # Get specific field
    name = r.hget("user:2", "name")
    print(f"✓ Get user:2 name -> {name}")
    print("  CLI: HGET user:2 name")
    
    # UPDATE - Modify documents
    print("\n--- UPDATE Operations ---")
    r.hset("user:1", "age", "26")
    print("  CLI: HSET user:1 age 26")
    r.hset("user:1", "department", "Engineering")
    print("  CLI: HSET user:1 department Engineering")
    print(f"✓ Updated user:1 -> {r.hgetall('user:1')}")
    
    # DELETE - Remove fields or entire document
    print("\n--- DELETE Operations ---")
    r.hdel("user:2", "city")
    print(f"✓ Deleted city from user:2 -> {r.hgetall('user:2')}")
    print("  CLI: HDEL user:2 city")
    
    r.delete("user:4")
    print(f"✓ Deleted entire user:4 document")
    print("  CLI: DEL user:4")

def demo_list_operations():
    """List operations (Ordered collections)"""
    print("\n" + "="*60)
    print("3. LIST OPERATIONS (Ordered Collections/Arrays)")
    print("="*60)
    
    # Add items to list (queue-like)
    r.rpush("tasks:pending", "Task 1: Design database schema")
    r.rpush("tasks:pending", "Task 2: Implement API")
    r.rpush("tasks:pending", "Task 3: Write tests")
    print("  CLI: RPUSH tasks:pending \"Task 1: Design database schema\"")
    print("  CLI: RPUSH tasks:pending \"Task 2: Implement API\"")
    r.lpush("tasks:pending", "Task 0: Setup project")  # Add to front
    print("  CLI: LPUSH tasks:pending \"Task 0: Setup project\"")
    
    print("\n✓ Task list:")
    tasks = r.lrange("tasks:pending", 0, -1)
    for i, task in enumerate(tasks):
        print(f"  {i+1}. {task}")
    print("  CLI: LRANGE tasks:pending 0 -1")
    
    # List length
    print(f"\n✓ Total tasks: {r.llen('tasks:pending')}")
    print("  CLI: LLEN tasks:pending")
    
    # Pop items
    first_task = r.lpop("tasks:pending")
    print(f"\n✓ Popped first task: {first_task}")
    print("  CLI: LPOP tasks:pending")
    print(f"✓ Remaining: {r.lrange('tasks:pending', 0, -1)}")

def demo_set_operations():
    """Set operations (Unique unordered collections)"""
    print("\n" + "="*60)
    print("4. SET OPERATIONS (Unique Collections)")
    print("="*60)
    
    # Add members to sets
    r.sadd("skills:python", "Alice", "Bob", "Carol")
    print("  CLI: SADD skills:python Alice Bob Carol")
    r.sadd("skills:javascript", "Bob", "Carol", "David")
    print("  CLI: SADD skills:javascript Bob Carol David")
    r.sadd("skills:java", "Alice", "David")
    print("  CLI: SADD skills:java Alice David")
    
    print("\n✓ Skills sets:")
    print(f"  Python developers: {r.smembers('skills:python')}")
    print("  CLI: SMEMBERS skills:python")
    print(f"  JavaScript developers: {r.smembers('skills:javascript')}")
    print(f"  Java developers: {r.smembers('skills:java')}")
    
    # Set operations
    print("\n--- Set Operations ---")
    both = r.sinter("skills:python", "skills:javascript")
    print(f"✓ Knows both Python AND JavaScript: {both}")
    print("  CLI: SINTER skills:python skills:javascript")
    
    either = r.sunion("skills:python", "skills:java")
    print(f"✓ Knows Python OR Java: {either}")
    print("  CLI: SUNION skills:python skills:java")
    
    only_python = r.sdiff("skills:python", "skills:javascript")
    print(f"✓ Knows only Python (not JS): {only_python}")
    print("  CLI: SDIFF skills:python skills:javascript")

def demo_sorted_set_operations():
    """Sorted Set operations (Sorted by score)"""
    print("\n" + "="*60)
    print("5. SORTED SET OPERATIONS (Leaderboards/Rankings)")
    print("="*60)
    
    # Add users with scores
    r.zadd("leaderboard:game1", {
        "Alice": 1500,
        "Bob": 2300,
        "Carol": 1800,
        "David": 2100,
        "Eve": 1950
    })
    print("  CLI: ZADD leaderboard:game1 1500 Alice 2300 Bob 1800 Carol 2100 David 1950 Eve")
    
    print("\n✓ Game leaderboard (highest to lowest):")
    leaderboard = r.zrevrange("leaderboard:game1", 0, -1, withscores=True)
    for rank, (name, score) in enumerate(leaderboard, 1):
        print(f"  {rank}. {name}: {int(score)} points")
    print("  CLI: ZREVRANGE leaderboard:game1 0 -1 WITHSCORES")
    
    # Range queries
    print("\n✓ Players with score between 1800-2200:")
    mid_range = r.zrangebyscore("leaderboard:game1", 1800, 2200, withscores=True)
    for name, score in mid_range:
        print(f"  {name}: {int(score)}")
    print("  CLI: ZRANGEBYSCORE leaderboard:game1 1800 2200 WITHSCORES")
    
    # Rank query
    rank = r.zrevrank("leaderboard:game1", "Carol")
    print(f"\n✓ Carol's rank: #{rank + 1}")
    print("  CLI: ZREVRANK leaderboard:game1 Carol")
    
    # Increment score
    r.zincrby("leaderboard:game1", 300, "Alice")
    new_score = r.zscore("leaderboard:game1", "Alice")
    print(f"✓ Alice's new score after +300: {int(new_score)}")
    print("  CLI: ZINCRBY leaderboard:game1 300 Alice")
    print("  CLI: ZSCORE leaderboard:game1 Alice")

def demo_search_and_filter():
    """Search and filter operations using patterns"""
    print("\n" + "="*60)
    print("6. SEARCH & FILTER OPERATIONS")
    print("="*60)
    
    # Pattern matching with SCAN
    print("\n--- Pattern Matching ---")
    user_keys = []
    for key in r.scan_iter("user:*"):
        user_keys.append(key)
    print(f"✓ Found {len(user_keys)} user keys: {user_keys}")
    print("  CLI: SCAN 0 MATCH user:* COUNT 100")
    print("  CLI: KEYS user:*  (use SCAN in production, not KEYS!)")
    
    # Filter users by field value
    print("\n--- Filter by Field Value ---")
    print("Developers in New York:")
    for key in r.scan_iter("user:*"):
        user_data = r.hgetall(key)
        if user_data.get("role") == "developer" and user_data.get("city") == "New York":
            print(f"  {key} -> {user_data.get('name')}")
    print("  Note: Filtering requires client-side logic with HGETALL")
    
    # Filter by age range
    print("\nUsers aged 25-30:")
    for key in r.scan_iter("user:*"):
        user_data = r.hgetall(key)
        age = int(user_data.get("age", 0))
        if 25 <= age <= 30:
            print(f"  {user_data.get('name')} (age {age})")
    print("  Note: Range queries require client-side filtering or RediSearch module")

def demo_json_operations():
    """Working with JSON data"""
    print("\n" + "="*60)
    print("7. JSON OPERATIONS (Complex Data Types)")
    print("="*60)
    
    # Store complex objects as JSON
    product = {
        "id": "prod_001",
        "name": "Laptop",
        "price": 999.99,
        "specs": {
            "ram": "16GB",
            "storage": "512GB SSD",
            "processor": "Intel i7"
        },
        "tags": ["electronics", "computers", "portable"],
        "in_stock": True
    }
    
    r.set("product:001", json.dumps(product))
    print("  CLI: SET product:001 '{\"id\":\"prod_001\",\"name\":\"Laptop\",...}'")
    
    # Retrieve and parse JSON
    retrieved = json.loads(r.get("product:001"))
    print("\n✓ Stored and retrieved complex JSON object:")
    print(json.dumps(retrieved, indent=2))
    print("  CLI: GET product:001")
    print("  Note: JSON stored as string, parsing done client-side")
    print("  For native JSON: Use RedisJSON module with JSON.SET/JSON.GET")

def demo_expiration():
    """TTL and expiration"""
    print("\n" + "="*60)
    print("8. EXPIRATION & TTL (Time-To-Live)")
    print("="*60)
    
    # Set key with expiration
    r.setex("session:user123", 300, "active")  # Expires in 300 seconds
    print("  CLI: SETEX session:user123 300 active")
    
    ttl = r.ttl("session:user123")
    print(f"\n✓ Session key will expire in {ttl} seconds")
    print("  CLI: TTL session:user123")
    
    # Set expiration on existing key
    r.set("temp:data", "temporary value")
    print("  CLI: SET temp:data \"temporary value\"")
    r.expire("temp:data", 60)
    print(f"✓ Temp data will expire in {r.ttl('temp:data')} seconds")
    print("  CLI: EXPIRE temp:data 60")
    print("  CLI: TTL temp:data")

def demo_transactions():
    """Transaction operations"""
    print("\n" + "="*60)
    print("9. TRANSACTIONS (MULTI/EXEC)")
    print("="*60)
    
    # Transfer points between users atomically
    pipe = r.pipeline()
    pipe.hincrby("user:1", "points", -100)
    pipe.hincrby("user:2", "points", 100)
    pipe.execute()
    
    print("\n✓ Atomic transaction completed:")
    print(f"  user:1 points: {r.hget('user:1', 'points')}")
    print(f"  user:2 points: {r.hget('user:2', 'points')}")
    print("\n  CLI Transaction:")
    print("  MULTI")
    print("  HINCRBY user:1 points -100")
    print("  HINCRBY user:2 points 100")
    print("  EXEC")

def demo_key_management():
    """Key management operations"""
    print("\n" + "="*60)
    print("10. KEY MANAGEMENT & STATISTICS")
    print("="*60)
    
    # Count keys
    total_keys = r.dbsize()
    print(f"\n✓ Total keys in database: {total_keys}")
    print("  CLI: DBSIZE")
    
    # Check if key exists
    exists = r.exists("user:1")
    print(f"✓ Key 'user:1' exists: {bool(exists)}")
    print("  CLI: EXISTS user:1")
    
    # Get key type
    key_type = r.type("user:1")
    print(f"✓ Type of 'user:1': {key_type}")
    print("  CLI: TYPE user:1")
    
    # List all keys (be careful with large databases!)
    print("\n✓ Sample of keys in database:")
    sample_keys = list(r.scan_iter(count=10))[:5]
    for key in sample_keys:
        print(f"  {key} ({r.type(key)})")
    print("  CLI: SCAN 0 COUNT 10")
    print("  CLI: KEYS *  (Warning: blocks server, use SCAN instead!)")

def main():
    """Run all demos"""
    try:
        # Test connection
        r.ping()
        print("✓ Connected to Redis successfully!")
        
        # Run all demos
        clear_demo_data()
        demo_string_operations()
        demo_hash_operations()
        demo_list_operations()
        demo_set_operations()
        demo_sorted_set_operations()
        demo_search_and_filter()
        demo_json_operations()
        demo_expiration()
        demo_transactions()
        demo_key_management()
        
        print("\n" + "="*60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except redis.ConnectionError:
        print("❌ Error: Could not connect to Redis.")
        print("Make sure Redis is running: sudo service redis-server start")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

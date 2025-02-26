"""
Memory hierarchy simulation for the CPU Pipeline Simulator.
Includes caches and main memory.
"""

class MemoryUnit:
    """Base class for memory units"""
    def __init__(self, name, access_time):
        self.name = name
        self.access_time = access_time  # In cycles
        self.reads = 0
        self.writes = 0
    
    def read(self, address):
        """Read data from memory"""
        self.reads += 1
        return None
    
    def write(self, address, data):
        """Write data to memory"""
        self.writes += 1
    
    def stats(self):
        """Return statistics about memory unit"""
        return {
            'name': self.name,
            'reads': self.reads,
            'writes': self.writes,
            'total_accesses': self.reads + self.writes
        }


class MainMemory(MemoryUnit):
    """Main memory implementation"""
    
    def __init__(self, access_time=100):
        super().__init__("Main Memory", access_time)
        self.data = {}
    
    def read(self, address):
        """Read data from main memory"""
        super().read(address)
        return self.data.get(address, 0)
    
    def write(self, address, data):
        """Write data to main memory"""
        super().write(address, data)
        self.data[address] = data


class CacheLine:
    """A single cache line"""
    
    def __init__(self, size=64):
        self.valid = False
        self.dirty = False
        self.tag = None
        self.data = {}  # Offset -> data
        self.size = size


class Cache(MemoryUnit):
    """Cache memory implementation"""
    
    def __init__(self, name, size, line_size, associativity, access_time, next_level=None):
        super().__init__(name, access_time)
        self.size = size  # Total size in bytes
        self.line_size = line_size  # Line size in bytes
        self.associativity = associativity  # Number of ways
        self.next_level = next_level  # Next level in memory hierarchy
        
        self.num_sets = size // (line_size * associativity)
        self.lines = [[CacheLine(line_size) for _ in range(associativity)] for _ in range(self.num_sets)]
        
        # Cache statistics
        self.hits = 0
        self.misses = 0
    
    def _get_cache_address(self, address):
        """Convert memory address to cache address (tag, set, offset)"""
        # Calculate bit widths
        offset_bits = self._log2(self.line_size)
        set_bits = self._log2(self.num_sets)
        
        # Extract address components
        offset = address & ((1 << offset_bits) - 1)
        set_index = (address >> offset_bits) & ((1 << set_bits) - 1)
        tag = address >> (offset_bits + set_bits)
        
        return tag, set_index, offset
    
    def _log2(self, x):
        """Calculate log base 2 of x"""
        return x.bit_length() - 1 if x > 0 else 0
    
    def _find_line(self, tag, set_index):
        """Find cache line with matching tag in the specified set"""
        for way, line in enumerate(self.lines[set_index]):
            if line.valid and line.tag == tag:
                return way, line
        return None, None
    
    def _evict_line(self, set_index):
        """Select a line to evict using LRU policy (simplified)"""
        # For now, just pick the first line (replace with actual LRU later)
        return 0, self.lines[set_index][0]
    
    def read(self, address):
        """Read data from cache"""
        super().read(address)
        
        tag, set_index, offset = self._get_cache_address(address)
        way, line = self._find_line(tag, set_index)
        
        # Cache hit
        if line:
            self.hits += 1
            return line.data.get(offset, 0)
        
        # Cache miss
        self.misses += 1
        
        # Fetch from next level
        data = 0
        if self.next_level:
            data = self.next_level.read(address)
        
        # Allocate a new line (with eviction if needed)
        way, line = self._evict_line(set_index)
        
        # Write back evicted line if dirty
        if line.valid and line.dirty and self.next_level:
            for off, d in line.data.items():
                evict_addr = ((line.tag << self._log2(self.num_sets)) | set_index) << self._log2(self.line_size) | off
                self.next_level.write(evict_addr, d)
        
        # Update cache line
        line.valid = True
        line.dirty = False
        line.tag = tag
        line.data = {}  # Clear old data
        line.data[offset] = data
        
        # Fill rest of the cache line (simplified)
        base_addr = address - offset
        for i in range(self.line_size):
            if i != offset and self.next_level:
                line.data[i] = self.next_level.read(base_addr + i)
        
        return data
    
    def write(self, address, data):
        """Write data to cache"""
        super().write(address, data)
        
        tag, set_index, offset = self._get_cache_address(address)
        way, line = self._find_line(tag, set_index)
        
        # Cache hit
        if line:
            self.hits += 1
            line.data[offset] = data
            line.dirty = True
            return
        
        # Cache miss
        self.misses += 1
        
        # Write-allocate policy: read the line first
        self.read(address)
        
        # Now we should have the line in cache
        way, line = self._find_line(tag, set_index)
        if line:
            line.data[offset] = data
            line.dirty = True
    
    def stats(self):
        """Return cache statistics"""
        base_stats = super().stats()
        hit_rate = self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0
        miss_rate = 1.0 - hit_rate
        
        return {
            **base_stats,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'miss_rate': miss_rate
        }


class MemoryHierarchy:
    """Complete memory hierarchy with caches and main memory"""
    
    def __init__(self, config=None):
        """Initialize the memory hierarchy"""
        if not config:
            # Default configuration
            config = {
                'l1': {'size': 32768, 'line_size': 64, 'associativity': 8, 'access_time': 1},
                'l2': {'size': 262144, 'line_size': 64, 'associativity': 8, 'access_time': 10},
                'main_memory': {'access_time': 100}
            }
        
        # Create memory hierarchy (bottom-up)
        self.main_memory = MainMemory(config['main_memory']['access_time'])
        
        if 'l2' in config:
            self.l2_cache = Cache(
                "L2 Cache",
                config['l2']['size'],
                config['l2']['line_size'],
                config['l2']['associativity'],
                config['l2']['access_time'],
                self.main_memory
            )
            next_level = self.l2_cache
        else:
            next_level = self.main_memory
        
        self.l1_cache = Cache(
            "L1 Cache",
            config['l1']['size'],
            config['l1']['line_size'],
            config['l1']['associativity'],
            config['l1']['access_time'],
            next_level
        )
    
    def read(self, address):
        """Read data from memory hierarchy"""
        return self.l1_cache.read(address)
    
    def write(self, address, data):
        """Write data to memory hierarchy"""
        self.l1_cache.write(address, data)
    
    def stats(self):
        """Return statistics for all levels of the memory hierarchy"""
        stats = {
            'l1': self.l1_cache.stats()
        }
        
        if hasattr(self, 'l2_cache'):
            stats['l2'] = self.l2_cache.stats()
        
        stats['main_memory'] = self.main_memory.stats()
        
        return stats

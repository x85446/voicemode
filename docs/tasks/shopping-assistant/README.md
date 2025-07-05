# Voice Mode Shopping Assistant

## Overview

A voice-enabled shopping assistant that helps users shop efficiently while having conversations. The assistant tracks shopping lists, compares prices between stores, understands pricing cycles, and guides users through the store - all through natural voice interaction.

## Core Features

### 1. Shopping List Management
- Maintain shopping list as a markdown file (e.g., `shopping-list.md`)
- Check off items as user mentions purchasing them
- Add new items on the fly
- Track quantities and preferences

### 2. Price Comparison MCP Tool
- Query current prices at major Australian supermarkets (Coles, Woolworths)
- Track high-low pricing cycles
  - Some items cycle weekly (Tuesday night changes)
  - Others cycle Sunday night
  - Can be 50% off one week, normal price the next
- Recommend which store to buy specific items from
- Alert user to wait for better prices on non-urgent items

### 3. Store Navigation
- Know store layouts (aisle information for common items)
- Optimize shopping route through the store
- Guide user to next item's location
- Handle different store layouts

### 4. Conversational Shopping
- Natural conversation while shopping
- Discuss recipes while finding ingredients
- Talk about other topics between shopping tasks
- Hands-free operation - perfect for pushing trolley

## Example Interaction

```
User: "I'm at Coles now, let's start shopping"
Assistant: "Great! I have your shopping list ready. Let's start with produce in aisle 1. 
            First item is bananas - they're $2.90/kg at Coles this week, which is good 
            since Woolworths has them at $3.50."

User: "Got the bananas, what's next?"
Assistant: "Bananas checked off! Next is milk. Head to aisle 8 - dairy section. 
            By the way, cheese is on special at Woolworths this week if you need any. 
            The vintage cheddar is half price until Tuesday."

User: "Oh that reminds me, I need to add eggs to the list"
Assistant: "Added eggs to your list. You'll find them in the same aisle as the milk."
```

## Technical Implementation

### Shopping List Format
```markdown
# Shopping List - 2025-01-05

## Produce
- [ ] Bananas (1kg)
- [x] Apples (6)
- [ ] Carrots

## Dairy  
- [ ] Milk (2L, full cream)
- [ ] Eggs (added via voice)

## Pantry
- [ ] Rice (basmati, 1kg)
- [ ] Pasta

## Notes
- Check cheese specials at Woolworths
- Laundry detergent if under $10
```

### MCP Tools Needed

#### 1. Shopping List Tool
```python
@mcp.tool()
async def shopping_list_update(
    action: Literal["check", "uncheck", "add", "remove", "show"],
    item: Optional[str] = None,
    category: Optional[str] = None
) -> str:
    """Manage the shopping list"""
```

#### 2. Price Checker Tool  
```python
@mcp.tool()
async def check_prices(
    item: str,
    stores: List[str] = ["coles", "woolworths"]
) -> Dict[str, float]:
    """Check current prices across stores"""
```

#### 3. Store Navigator Tool
```python
@mcp.tool() 
async def find_item_location(
    item: str,
    store: str
) -> str:
    """Get aisle/location for item in specific store"""
```

## Data Sources

### Price Data Options
1. Web scraping store websites (with appropriate rate limiting)
2. Community-maintained price database
3. Receipt OCR from previous shops
4. Manual price tracking with pattern detection

### Store Layout Data
1. Crowdsourced aisle information
2. Store-specific apps/APIs if available
3. Common patterns (dairy always refrigerated section, etc.)

## Privacy Considerations
- Shopping data stored locally only
- No personal information in price queries
- Optional anonymized price sharing to help community

## Future Enhancements
1. Recipe integration - suggest items for planned meals
2. Budget tracking - running total while shopping
3. Dietary preferences - highlight suitable items
4. Stock tracking - remember what's at home
5. Multi-store routes - optimize across multiple stops
6. Barcode scanning integration for price verification

## Benefits
- Save money through price awareness
- Save time through efficient routing  
- Make shopping less tedious with conversation
- Reduce forgotten items
- Discover deals you might miss
- Turn "dead time" into productive/social time

## Use Cases Beyond Supermarkets
- Hardware store projects (tracking parts needed)
- Clothes shopping (size/color preferences)
- Pharmacy runs (prescription reminders)
- Farmers markets (seasonal availability)
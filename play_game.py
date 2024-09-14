from DeckOfCards import DeckOfCards

#Define Score of the Game
def calculate_score(cards):
    score = 0
    ace_count = 0
    
    for card in cards:
        value = card.get_value()
        score += value
        if card.rank == 'Ace':
            ace_count += 1
    
# Adjust for Aces if the score exceeds 21
    while score > 21 and ace_count > 0:
        score -= 10
        ace_count -= 1
    
    return score

def play_blackjack():
    print("Welcome to Blackjack!")
    
# Create and shuffle the deck
    deck = DeckOfCards()
    print("Deck before shuffle:")
    print(deck)
    
    deck.shuffle_deck()
    
    print("\nDeck after shuffle:")
    print(deck)
    
    while True:
        user_cards = [deck.get_card(), deck.get_card()]
        dealer_cards = [deck.get_card(), deck.get_card()]

# Define the Player's turn
        print(f"\nYour cards: {user_cards[0]}, {user_cards[1]}")
        user_score = calculate_score(user_cards)
        print(f"Your total score: {user_score}")
        
        while user_score <= 21:
            choice = input("Would you like a hit? (y/n) ")
            if choice == 'y':
                new_card = deck.get_card()
                user_cards.append(new_card)
                print(f"Card drawn: {new_card}")
                user_score = calculate_score(user_cards)
                print(f"Your total score: {user_score}")
            else:
                break
        
        if user_score > 21:
            print("You busted. You lose")
        else:
# Define the Dealer's turn
            print("\nDealer's turn...")
            dealer_score = calculate_score(dealer_cards)
            print(f"Dealer's cards: {dealer_cards[0]}, {dealer_cards[1]}")
            
            while dealer_score < 17:
                new_card = deck.get_card()
                dealer_cards.append(new_card)
                print(f"Dealer draws: {new_card}")
                dealer_score = calculate_score(dealer_cards)
            
            print(f"Dealer's total score: {dealer_score}")
            
            if dealer_score > 21:
                print("Dealer busted. You win")
            elif user_score > dealer_score:
                print("You win")
            else:
                print("Dealer wins")
        
        play_again = input("Play again? (y/n) ")
        if play_again != 'y':
            break
        else:
            deck.shuffle_deck()

if __name__ == "__main__":
    play_blackjack()
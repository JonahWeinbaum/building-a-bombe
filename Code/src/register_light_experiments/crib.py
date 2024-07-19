import networkx as nx
import matplotlib.pyplot as plt

def generate_valid_crib_pairings(encrypted_text, crib):
    # Remove spaces from both the encrypted text and the crib
    encrypted_text = encrypted_text.replace(" ", "")
    crib = crib.replace(" ", "")

    pairings = []

    for i in range(len(encrypted_text) - len(crib) + 1):
        substring = encrypted_text[i:i + len(crib)]
        
        # Check if the pairing is valid
        valid = True
        for j in range(len(crib)):
            if substring[j] == crib[j]:
                valid = False
                break
        
        if valid:
            pairings.append((substring, crib, i))
    return pairings

# Example usage:
encrypted_text = "LANOTCTOUARBBFPMHPHGCZXTDYGAHGUFXGEWKBLKGJWLQXXTGPJJAV"
crib = "ISTSOFORTBEKANNTZUGEBENXX"

pairings = generate_valid_crib_pairings(encrypted_text, crib)
# for idx, (cipher, plain) in enumerate(pairings):
#     print(f"Pairing {idx + 1}: Cipher = {cipher}, Plain = {plain}")


def visualize_pairing(pairing):
    G = nx.DiGraph()

    if pairing is not None:
        cipher, plain, start_index = pairing
        for i, (c, p) in enumerate(zip(cipher, plain)):
            G.add_edge(p, c, label=start_index + i)
        
        pos = nx.kamada_kawai_layout(G)  # Use spring layout for better visualization
        edge_labels = nx.get_edge_attributes(G, 'label')
        
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=30, font_size=15, font_weight='bold', edge_color='gray')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
        plt.title("Plaintext-Ciphertext Pairing Visualization")
        plt.show()
    else:
        print("No valid pairing found.")


visualize_pairing(pairings[0])
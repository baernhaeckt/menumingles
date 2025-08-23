import torch
import torch.nn as nn
import torch.nn.functional as F

class RecipeEmbeddingModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, projection_dim=128, pooling="mean"):
        super().__init__()
        self.pooling = pooling
        self.embedding = nn.Embedding(vocab_size, embedding_dim)

        # Projection head (SimCLR style)
        self.projection = nn.Sequential(
            nn.Linear(embedding_dim, embedding_dim),
            nn.ReLU(),
            nn.Linear(embedding_dim, projection_dim)
        )

        if pooling == "attention":
            self.attention = nn.Linear(embedding_dim, 1)

    def forward(self, ingredient_indices):
        # Pad variable-length ingredient lists
        padded = nn.utils.rnn.pad_sequence(
            [torch.tensor(x) for x in ingredient_indices],
            batch_first=True,
            padding_value=0
        )
        mask = (padded != 0)  # padding mask
        embeds = self.embedding(padded)

        if self.pooling == "attention":
            # Compute attention scores
            attn_logits = self.attention(embeds).squeeze(-1)  # [batch, seq_len]
            attn_logits[mask == 0] = -1e9  # mask padding
            attn_weights = F.softmax(attn_logits, dim=1).unsqueeze(-1)  # [batch, seq_len, 1]
            recipe_embeds = (embeds * attn_weights).sum(1)
        elif self.pooling == "mean":
            # Mean pooling over ingredients
            masked_embeds = embeds * mask.unsqueeze(-1)
            recipe_embeds = masked_embeds.sum(1) / (mask.sum(1, keepdim=True) + 1e-8)
        else:
            raise NotImplementedError(f"Unknown pool_type: {self.pooling}")

        # normalize for cosine similarity
        recipe_embeds = F.normalize(recipe_embeds, dim=-1)

        # Projection for contrastive loss
        projected = self.projection(recipe_embeds)
        projected = F.normalize(projected, dim=-1)  # keep cosine scale

        return recipe_embeds, projected
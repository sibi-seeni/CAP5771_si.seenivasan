"""
RoBERTa Sentiment Classification Script
========================================
Optimized for Apple Silicon (M1/M2/M3) with MPS acceleration, with option for CUDA.
Uses TweetNLP library for cardiffnlp/twitter-roberta-base-sentiment-latest.

Author: Sibi Seenivasan
Date: March 2026
"""

import tweetnlp
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

def setup_roberta():
    print("=" * 80)
    print("INITIALIZING ROBERTA MODEL")
    print("=" * 80)
    
    # Check for device availability
    import torch
    
    if torch.backends.mps.is_available():
        device = "mps"
        print("✅ Apple Silicon detected - using MPS acceleration")
    elif torch.cuda.is_available():
        device = "cuda"
        print("✅ CUDA GPU detected - using GPU acceleration")
    else:
        device = "cpu"
        print("⚠️  Using CPU (consider using Apple Silicon or CUDA for speedup)")
    
    print(f"   Device: {device}")
    
    # Load sentiment model (TweetNLP handles device automatically)
    print("\nLoading cardiffnlp/twitter-roberta-base-sentiment-latest...")
    model = tweetnlp.Sentiment()
    
    # Move model to appropriate device
    if hasattr(model, 'model'):
        model.model = model.model.to(device)
        print(f"✅ RoBERTa model loaded and moved to {device}")
    else:
        print("✅ RoBERTa model loaded (device auto-detected)")
    
    print("   Model: cardiffnlp/twitter-roberta-base-sentiment-latest")
    print("=" * 80 + "\n")
    
    return model, device

def classify_roberta_batch(texts, model, batch_size=256, show_progress=True):
    """
    Classify texts using RoBERTa with full probability distribution.
    
    Args:
        texts: NumPy array or list of text strings
        model: TweetNLP sentiment model
        batch_size: Number of texts to process at once (256-512 for MPS/GPU)
        show_progress: Whether to show progress bar
    
    Returns:
        results: DataFrame with probabilities and predictions
    """
    import torch
    from tqdm.auto import tqdm
    
    n = len(texts)
    
    # Pre-allocate NumPy arrays (much faster than appending to lists)
    neg = np.zeros(n, dtype=np.float32)
    neu = np.zeros(n, dtype=np.float32)
    pos = np.zeros(n, dtype=np.float32)
    conf = np.zeros(n, dtype=np.float32)
    labels = np.zeros(n, dtype=np.int8)
    
    print(f"Classifying {n:,} texts with RoBERTa...")
    print(f"Batch size: {batch_size} (optimized for speed)")
    print(f"Total batches: {(n + batch_size - 1) // batch_size:,}\n")
    
    iterator = range(0, n, batch_size)
    if show_progress:
        iterator = tqdm(iterator, desc="Processing batches", total=(n + batch_size - 1) // batch_size)
    
    idx = 0
    
    # Disable gradient computation for inference (saves memory and speeds up)
    with torch.no_grad():
        for i in iterator:
            batch = texts[i:i + batch_size]
            
            try:
                # Predict with TweetNLP - returns probability distribution
                preds = model.sentiment(batch, return_probability=True)
                
                # Extract probabilities efficiently
                batch_neg = []
                batch_neu = []
                batch_pos = []
                
                for p in preds:
                    probs = p["probability"]
                    batch_neg.append(probs["negative"])
                    batch_neu.append(probs["neutral"])
                    batch_pos.append(probs["positive"])
                
                # Convert to NumPy arrays
                batch_neg = np.array(batch_neg, dtype=np.float32)
                batch_neu = np.array(batch_neu, dtype=np.float32)
                batch_pos = np.array(batch_pos, dtype=np.float32)
                
                size = len(batch)
                
                # Store probabilities
                neg[idx:idx + size] = batch_neg
                neu[idx:idx + size] = batch_neu
                pos[idx:idx + size] = batch_pos
                
                # Vectorized label and confidence computation
                probs = np.vstack([batch_neg, batch_neu, batch_pos]).T
                label_idx = np.argmax(probs, axis=1)
                
                # Confidence is max probability
                conf[idx:idx + size] = probs[np.arange(size), label_idx]
                
                # Map label indices to sentiment values: 0->-1, 1->0, 2->1
                labels[idx:idx + size] = np.select(
                    [label_idx == 0, label_idx == 1, label_idx == 2],
                    [-1, 0, 1]
                )
                
                idx += size
                
            except Exception as e:
                print(f"\n⚠️  Error in batch starting at index {i}: {e}")
                # Skip this batch (arrays already initialized to 0)
                idx += len(batch)
    
    return pd.DataFrame({
        'roberta_sentiment_neg': neg,
        'roberta_sentiment_neu': neu,
        'roberta_sentiment_pos': pos,
        'roberta_sentiment_label': labels,
        'roberta_confidence': conf
    })

def main(input_file='data/comments_for_analysis.csv',
         output_file='data/roberta_classifications.csv',
         batch_size=32,
         sample_size=None):
    """
    Main RoBERTa classification pipeline.
    
    Args:
        input_file: Path to input CSV
        output_file: Path to save results
        batch_size: Batch size for processing (default 32, increase for MPS/GPU)
        sample_size: If provided, only classify first N rows (for testing)
    """
    import time
    
    print("\n" + "=" * 80)
    print("ROBERTA SENTIMENT CLASSIFICATION")
    print("=" * 80 + "\n")
    
    start_time = time.time()
    
    # Load data
    print(f"Loading data from {input_file}...")
    if not os.path.exists(input_file):
        print(f"❌ Error: File not found: {input_file}")
        return None
    
    df = pd.read_csv(input_file)
    print(f"✅ Loaded {len(df):,} rows")
    
    # Check required column
    if 'text_preprocessed' not in df.columns:
        print("❌ Error: 'text_preprocessed' column not found in data")
        print(f"Available columns: {', '.join(df.columns)}")
        return None
    
    # Sample if requested
    if sample_size and sample_size < len(df):
        print(f"\n⚠️  Using sample of {sample_size:,} rows for testing")
        df = df.head(sample_size).copy()
    
    print()
    
    # Setup model
    model, device = setup_roberta()
    
    # Adjust batch size for device
    if device == "mps":
        # Apple Silicon can handle much larger batches
        recommended_batch_size = 256  # Optimized for MPS
        print(f"💡 Tip: Apple Silicon detected. Recommended batch size: {recommended_batch_size}")
        print(f"   Can try up to 512 for very short comments\n")
        if batch_size < recommended_batch_size:
            batch_size = recommended_batch_size
            print(f"   Using batch size: {batch_size}\n")
    elif device == "cuda":
        recommended_batch_size = 512  # CUDA can handle large batches
        print(f"💡 Tip: GPU detected. Recommended batch size: {recommended_batch_size}")
        print(f"   Can try up to 1024 for very short comments\n")
        if batch_size < recommended_batch_size:
            batch_size = recommended_batch_size
            print(f"   Using batch size: {batch_size}\n")
    else:
        # CPU should use smaller batches
        recommended_batch_size = 64
        print(f"💡 Tip: CPU detected. Recommended batch size: {recommended_batch_size}\n")
        if batch_size > recommended_batch_size:
            batch_size = recommended_batch_size
            print(f"   Using batch size: {batch_size}\n")
    
    # Prepare texts - use NumPy array for efficiency
    texts = df['text_preprocessed'].fillna('').astype(str).values
    print(f"Prepared {len(texts):,} texts as NumPy array for efficient processing\n")
    
    # Classify
    classification_start = time.time()
    results_df = classify_roberta_batch(texts, model, batch_size=batch_size)
    classification_time = time.time() - classification_start
    
    # Combine with original data
    df_output = pd.concat([df, results_df], axis=1)
    
    # Print summary statistics
    print("\n" + "=" * 80)
    print("CLASSIFICATION RESULTS")
    print("=" * 80)
    
    print(f"\nSentiment Distribution:")
    print("-" * 80)
    for label, name in [(-1, 'Negative'), (0, 'Neutral'), (1, 'Positive')]:
        count = (df_output['roberta_sentiment_label'] == label).sum()
        pct = count / len(df_output) * 100
        print(f"  {name:12s}: {count:>8,} ({pct:>5.2f}%)")
    
    print(f"\nConfidence Statistics:")
    print("-" * 80)
    print(f"  Mean confidence:       {df_output['roberta_confidence'].mean():>6.3f}")
    print(f"  Median confidence:     {df_output['roberta_confidence'].median():>6.3f}")
    print(f"  Min confidence:        {df_output['roberta_confidence'].min():>6.3f}")
    print(f"  Max confidence:        {df_output['roberta_confidence'].max():>6.3f}")
    
    high_conf = (df_output['roberta_confidence'] > 0.70).sum()
    medium_conf = ((df_output['roberta_confidence'] > 0.50) & 
                   (df_output['roberta_confidence'] <= 0.70)).sum()
    low_conf = (df_output['roberta_confidence'] <= 0.50).sum()
    
    print(f"\nConfidence Distribution:")
    print("-" * 80)
    print(f"  High (>0.70):          {high_conf:>8,} ({high_conf/len(df_output)*100:>5.2f}%)")
    print(f"  Medium (0.50-0.70):    {medium_conf:>8,} ({medium_conf/len(df_output)*100:>5.2f}%)")
    print(f"  Low (≤0.50):           {low_conf:>8,} ({low_conf/len(df_output)*100:>5.2f}%)")
    
    print(f"\nProbability Distribution Statistics:")
    print("-" * 80)
    print(f"  Avg P(Negative):       {df_output['roberta_sentiment_neg'].mean():>6.3f}")
    print(f"  Avg P(Neutral):        {df_output['roberta_sentiment_neu'].mean():>6.3f}")
    print(f"  Avg P(Positive):       {df_output['roberta_sentiment_pos'].mean():>6.3f}")
    
    # Save results
    print("\n" + "=" * 80)
    print("SAVING RESULTS")
    print("=" * 80 + "\n")
    
    # Create output directory if needed
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✅ Created directory: {output_dir}")
    
    df_output.to_csv(output_file, index=False)
    print(f"✅ Saved: {output_file}")
    print(f"   Rows: {len(df_output):,}")
    print(f"   Columns: {len(df_output.columns)}")
    
    # Save summary statistics
    summary_file = output_file.replace('.csv', '_summary.txt')
    with open(summary_file, 'w') as f:
        f.write("ROBERTA CLASSIFICATION SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Input file:        {input_file}\n")
        f.write(f"Output file:       {output_file}\n")
        f.write(f"Total comments:    {len(df_output):,}\n")
        f.write(f"Device:            {device}\n")
        f.write(f"Batch size:        {batch_size}\n")
        f.write(f"Processing time:   {classification_time:.1f} seconds ({classification_time/60:.1f} minutes)\n")
        f.write(f"Speed:             {len(df_output)/classification_time:.1f} comments/second\n\n")
        
        f.write("SENTIMENT DISTRIBUTION\n")
        f.write("-" * 80 + "\n")
        for label, name in [(-1, 'Negative'), (0, 'Neutral'), (1, 'Positive')]:
            count = (df_output['roberta_sentiment_label'] == label).sum()
            pct = count / len(df_output) * 100
            f.write(f"{name:12s}: {count:>8,} ({pct:>5.2f}%)\n")
        
        f.write("\nCONFIDENCE STATISTICS\n")
        f.write("-" * 80 + "\n")
        f.write(f"Mean:              {df_output['roberta_confidence'].mean():.3f}\n")
        f.write(f"Median:            {df_output['roberta_confidence'].median():.3f}\n")
        f.write(f"High (>0.70):      {high_conf:,} ({high_conf/len(df_output)*100:.2f}%)\n")
        f.write(f"Medium (0.50-0.70): {medium_conf:,} ({medium_conf/len(df_output)*100:.2f}%)\n")
        f.write(f"Low (≤0.50):       {low_conf:,} ({low_conf/len(df_output)*100:.2f}%)\n")
    
    print(f"✅ Saved summary: {summary_file}\n")
    
    # Performance statistics
    total_time = time.time() - start_time
    
    print("=" * 80)
    print("PERFORMANCE STATISTICS")
    print("=" * 80)
    print(f"\nTotal time:            {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    print(f"Classification time:   {classification_time:.1f} seconds ({classification_time/60:.1f} minutes)")
    print(f"Processing speed:      {len(df_output)/classification_time:.1f} comments/second")
    
    if sample_size is None:
        print(f"\n💡 For full dataset ({len(df):,} comments), estimated time:")
        print(f"   ~{(len(df)/len(df_output)) * classification_time / 60:.1f} minutes")
    
    print("\n" + "=" * 80)
    print("✅ CLASSIFICATION COMPLETE")
    print("=" * 80 + "\n")
    
    return df_output

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='RoBERTa sentiment classification (optimized for Apple Silicon)'
    )
    parser.add_argument('--input', type=str, 
                       default='data/comments_for_analysis.csv',
                       help='Input CSV file path')
    parser.add_argument('--output', type=str, 
                       default='data/roberta_classifications.csv',
                       help='Output CSV file path')
    parser.add_argument('--batch-size', type=int, default=256,
                       help='Batch size (default 256, auto-adjusted for device: CPU=64, MPS=256, CUDA=512)')
    parser.add_argument('--sample', type=int, default=None,
                       help='Process only first N rows (for testing)')
    
    args = parser.parse_args()
    
    # Run classification
    df_classified = main(
        input_file=args.input,
        output_file=args.output,
        batch_size=args.batch_size,
        sample_size=args.sample
    )
    
    if df_classified is not None:
        print("NEXT STEPS:")
        print("-" * 80)
        print("\n1. Apply confidence filtering (>0.7):")
        print("   df_confident = df[df['roberta_confidence'] > 0.7]")
        print(f"   → This will give you ~{(df_classified['roberta_confidence'] > 0.7).sum():,} high-confidence predictions")
        
        print("\n2. Analyze sentiment over time:")
        print("   daily_sentiment = df.groupby('comment_date')['roberta_sentiment_label'].mean()")
        
        print("\n3. Calculate popularity-weighted sentiment:")
        print("   weighted = (df['roberta_sentiment_label'] * df['likes']).sum() / df['likes'].sum()")
        
        print("\n4. Run Gemma classification separately:")
        print("   sbatch gemma_classification.sh")
        
        print("\n" + "=" * 80 + "\n")
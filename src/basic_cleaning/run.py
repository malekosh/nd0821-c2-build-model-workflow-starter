#!/usr/bin/env python
"""
download raw data from wb abd apply some basic cleaning
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    logger.info("creating wb run")
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)
    logger.info("downloading artifact")
    local_path = wandb.use_artifact("sample.csv:latest").file()
    
    logger.info("cleaning dataset")
    df = pd.read_csv(local_path)
    
    min_price = args.min_price
    max_price = args.max_price
    
    idx = df['price'].between(min_price,max_price)
    df = df[idx].copy()
    df['last_review'] = pd.to_datetime(df['last_review'])
    
    df.to_csv("clean_sample.csv", index=False)
    
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    logger.info("adding artifact")
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
        


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="the name of the raw dataset",
        required=True
    )
    
    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="the type of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="the description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="the minimum price of airbnbs",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="the max price of airbnbs",
        required=True
    )


    args = parser.parse_args()

    go(args)

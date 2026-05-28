#!/usr/bin/python3

import httpx
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from pathlib import Path
from tqdm import tqdm

# defines arguments to be used
def parseArgs():
    parser = argparse.ArgumentParser(description='Web scanner')
    parser.add_argument("source", help="Source URLs file")
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    parser.add_argument('-f', '--filters', help='Filters results by its response code')
    parser.add_argument('-o', '--output', help='Output file', default='workingUrls.txt')
    parser.add_argument('-t', '--threads', help='Number of threads to be deployed', default=10)
    parser.add_argument('--force-https', action='store_true', help='Adds http:// to URLs')
    return parser.parse_args()

# reads source file (txt) line by line
def readSource(sourceFile):
    with open(sourceFile, 'r') as webstxt:
        return webstxt.read().splitlines()

# adds the respective result to the output file
def addToOutput(code, url, outputFile, response):
    with open(outputFile, 'a') as of: # open output file as append mode!! IMPORTANT!!
        if code == 301: # if code == 301 adds the specific redirection line
            of.write(f'[{code}] - {url} -> {response.next_request.url}\n')
        else: 
            of.write(f'[{code}] - {url}\n')

# makes the request of the corresoponding URL
def requestUrl(url, filters, verbose=False, outputFile="workingUrls.txt"):
    try:
        response = httpx.get(url, timeout=10)
        code = response.status_code

        if verbose and not filters:
            print(f"[{code}] - {url}")

        elif verbose and filters:
            if str(code) in filters:
                print(f"[{code}] - {url}")

        if filters and str(code) in str(filters):
            addToOutput(code, url, outputFile, response)

        elif filters is None:
            addToOutput(code, url, outputFile, response)

    except Exception as e:
        if verbose and filters:
            pass
        elif verbose and not filters:    
            print(f"[{e.__class__.__name__}] - {url}")
        if (verbose or not verbose) and not filters:
            addToOutput((e.__class__.__name__), url, outputFile, None)

# adds https:// at the front of each url
def forceHTTP(urls):
    for i, url in enumerate(urls):
        if not url.startswith('https://'):
            urls[i] = 'https://' + url

# manages the flow of the tool
def main():
    args = parseArgs()
    urls = readSource(args.source)
    filters = args.filters if args.filters else None
    output = Path.cwd() / args.output

    if args.force_https: 
        forceHTTP(urls)

    if output.exists():
        output.unlink()

    if args.verbose:
            with ThreadPoolExecutor(max_workers=int(args.threads)) as executor:
                for url in urls:
                    executor.submit(requestUrl, url, filters, args.verbose, output)
    else:
        with ThreadPoolExecutor(max_workers=int(args.threads)) as executor:
            futures = [executor.submit(requestUrl, url, filters, args.verbose, output) for url in urls]
            for _ in tqdm(as_completed(futures), total=len(futures), desc="Scanning"):
                pass  

if __name__ == "__main__":
    main()

#franlumer-18/052025

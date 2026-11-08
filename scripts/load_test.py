"""Read-only concurrent requests for a classroom scalability experiment."""
import argparse
import asyncio
import statistics
import time
import httpx

async def run(url,total,concurrency):
    semaphore=asyncio.Semaphore(concurrency)
    timings=[];errors=0
    async with httpx.AsyncClient(timeout=10) as client:
        async def one(_):
            nonlocal errors
            async with semaphore:
                start=time.perf_counter()
                try:
                    response=await client.get(url)
                    if response.status_code!=200:errors+=1
                except httpx.RequestError:errors+=1
                timings.append((time.perf_counter()-start)*1000)
        start=time.perf_counter()
        await asyncio.gather(*(one(i) for i in range(total)))
        duration=time.perf_counter()-start
    success=total-errors
    p95=sorted(timings)[int(.95*(len(timings)-1))] if timings else 0
    print(f'total={total} success={success} errors={errors} duration_s={duration:.2f} '
          f'throughput_rps={total/duration:.1f} avg_ms={statistics.mean(timings):.1f} p95_ms={p95:.1f}')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--url',default='http://127.0.0.1:8080/api/catalog/restaurants')
    parser.add_argument('--requests',type=int,default=200)
    parser.add_argument('--concurrency',type=int,default=20)
    args=parser.parse_args()
    if args.requests<1 or args.concurrency<1:parser.error('Requests and concurrency must be positive')
    asyncio.run(run(args.url,args.requests,args.concurrency))

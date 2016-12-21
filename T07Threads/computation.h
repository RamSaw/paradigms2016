#ifndef T07THREADS_COMPUTATION_H
#define T07THREADS_COMPUTATION_H

#include <stdbool.h>
#include <pthread.h>
#include "./thread_pool/thread_pool.h"

typedef void (*OnComputationComplete)(void*);

struct Computation {
    void (*f)(void*);
    void *arg;

    struct Task task;
    pthread_mutex_t guard;
    pthread_cond_t finished_cond;
    bool finished;

    OnComputationComplete on_complete;
    void* on_complete_args;
};

void thpool_submit_computation(struct ThreadPool *pool, struct Computation *computation,
                               OnComputationComplete on_complete, void* on_complete_arg);
void thpool_complete_computation(struct Computation *computation);
void thpool_wait_computation(struct Computation *computation);


#endif /* T07THREADS_COMPUTATION_H */

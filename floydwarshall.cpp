
#include <math.h>
#include <string.h>

void floydwarshall(int nn, double m_adj[], double dist[], int pred[])
{
  
  memset(dist, 0, sizeof(double)*nn*nn);
  memset(pred, 0, sizeof(int)*nn*nn);
  
  for (int i=0; i < nn; i++) {
    for (int j=0; j < nn; j++) {
      dist[i*nn+j] = (m_adj[i*nn+j] != 0.0)? m_adj[i*nn+j] : INFINITY/2;
      
      if (i==j)  //diagonal case
	dist[i*nn+j] = 0.0;
      
      if ((dist[i*nn + j] > 0.0) && (dist[i*nn+j] < INFINITY/2))
	{
	  pred[i*nn+j] = i;
	}
      else
	{
	  pred[i*nn+j] = -1;
	}
      
    }
  }
  
  //Main loop of the algorithm
  for (int k=0; k < nn; k++) {
    for (int i=0; i < nn; i++) {
      for (int j=0; j < nn; j++) {
	double new_dist = dist[i*nn+k] + dist[k*nn+j];
	if (dist[i*nn+j] > new_dist) {
	  dist[i*nn+j] = new_dist;
	  pred[i*nn+j] = k;
	}
      }
    }
  }
  
}

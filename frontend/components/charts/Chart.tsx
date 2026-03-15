'use client';
import { useEffect, useRef } from 'react';
import { cn } from '@/lib/utils';

interface ChartProps {
  option: any;
  className?: string;
  height?: string;
}

export default function Chart({ option, className, height = '320px' }: ChartProps) {
  const chartRef = useRef<HTMLDivElement>(null);
  const instanceRef = useRef<any>(null);

  useEffect(() => {
    let mounted = true;

    async function init() {
      if (!chartRef.current || !mounted) return;
      const echartsModule = await import('echarts');
      const echarts = echartsModule.default || echartsModule;

      if (instanceRef.current) {
        instanceRef.current.dispose();
      }

      instanceRef.current = echarts.init(chartRef.current, undefined, { renderer: 'canvas' });

      const themed = {
        backgroundColor: 'transparent',
        textStyle: { color: '#8896ab', fontFamily: 'DM Sans' },
        legend: { textStyle: { color: '#8896ab' } },
        tooltip: {
          backgroundColor: '#1a2234',
          borderColor: '#1e2d45',
          textStyle: { color: '#e2e8f0', fontSize: 12 },
        },
        xAxis: { axisLine: { lineStyle: { color: '#1e2d45' } }, axisLabel: { color: '#8896ab' }, splitLine: { lineStyle: { color: '#1e2d4520' } } },
        yAxis: { axisLine: { lineStyle: { color: '#1e2d45' } }, axisLabel: { color: '#8896ab' }, splitLine: { lineStyle: { color: '#1e2d4520' } } },
        ...option,
      };

      instanceRef.current.setOption(themed, true);
    }

    init();

    const handleResize = () => {
      if (instanceRef.current) {
        instanceRef.current.resize();
      }
    };
    window.addEventListener('resize', handleResize);

    return () => {
      mounted = false;
      window.removeEventListener('resize', handleResize);
      if (instanceRef.current) {
        instanceRef.current.dispose();
        instanceRef.current = null;
      }
    };
  }, [option]);

  return <div ref={chartRef} className={cn('w-full', className)} style={{ height }} />;
}

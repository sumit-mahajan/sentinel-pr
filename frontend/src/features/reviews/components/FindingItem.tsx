import type { FindingDTO } from '@/shared/types/api';
import { Badge } from '@/shared/components/Badge';
import { Card } from '@/shared/components/Card';

export function FindingItem({ finding }: { finding: FindingDTO }) {
  return (
    <Card className="space-y-2">
      <div className="flex items-center gap-2">
        <Badge severity={finding.severity}>{finding.severity}</Badge>
        <span className="text-xs uppercase text-muted-foreground">{finding.category}</span>
        <span className="text-xs text-muted-foreground">via {finding.agent_source}</span>
      </div>
      <h4 className="font-medium">{finding.title}</h4>
      <p className="text-sm text-muted-foreground">
        <code>{finding.file_path}</code>
        {finding.line_start ? `:${finding.line_start}` : ''}
      </p>
      <p className="text-sm">{finding.description}</p>
      {finding.fix_suggestion && (
        <p className="rounded-md bg-muted/50 p-2 text-sm">
          <span className="font-medium">Fix: </span>
          {finding.fix_suggestion}
        </p>
      )}
    </Card>
  );
}
